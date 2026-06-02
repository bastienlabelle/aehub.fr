from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, EmailStr
from decimal import Decimal
from datetime import date
from typing import Any

from db.session import get_db
from db.models.client import Client
from db.models.invoice import Invoice
from db.models.line import Line
from db.models.user import User
from auth.dependencies import get_current_user
from schemas.data_import import ImportPayload, ImportResult

router = APIRouter(prefix="/import", tags=["import"])


@router.post("/", response_model=ImportResult)
async def import_data(
    payload: ImportPayload,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = ImportResult(
        clients_created=0,
        clients_updated=0,
        invoices_created=0,
        invoices_skipped=0,
        errors=[],
    )

    # Map email -> client_id pour les invoices
    client_map: dict[str, int] = {}

    # Import clients
    for c in payload.clients:
        existing = await db.execute(
            select(Client).where(
                Client.email == c.email,
                Client.user_id == current_user.id
            )
        )
        client = existing.scalar_one_or_none()
        # Nettoie siret et siren
        if c.siret:
            c.siret = c.siret.replace(' ', '')
        if c.siren:
            c.siren = c.siren.replace(' ', '')
        if c.phone:
            c.phone = c.phone.replace(' ', '')
        if c.zip_code:
            c.zip_code = c.zip_code.replace(' ', '')
        if client:
            for key, value in c.model_dump().items():
                setattr(client, key, value)
            result.clients_updated += 1
        else:
            client = Client(**c.model_dump(), user_id=current_user.id)
            db.add(client)
            result.clients_created += 1

        await db.flush()
        client_map[c.email] = client.id

    # Import invoices
    for inv in payload.invoices:
        # Vérifie si le numéro existe déjà
        existing = await db.execute(
            select(Invoice).where(
                Invoice.number == inv.number,
                Invoice.user_id == current_user.id
            )
        )
        if existing.scalar_one_or_none():
            result.invoices_skipped += 1
            result.errors.append(f"Facture {inv.number} déjà existante, ignorée")
            continue

        # Résout le client
        client_id = client_map.get(inv.client_ref)
        if not client_id:
            # Cherche en DB
            existing_client = await db.execute(
                select(Client).where(
                    Client.email == inv.client_ref,
                    Client.user_id == current_user.id
                )
            )
            client = existing_client.scalar_one_or_none()
            if not client:
                result.errors.append(f"Client '{inv.client_ref}' introuvable pour la facture {inv.number}")
                result.invoices_skipped += 1
                continue
            client_id = client.id

        invoice = Invoice(
            user_id=current_user.id,
            client_id=client_id,
            number=inv.number,
            subject=inv.subject,
            issued_at=inv.issued_at,
            due_date=inv.due_date,
            status=inv.status,
            notes=inv.notes,
        )
        db.add(invoice)
        await db.flush()

        for line_data in inv.lines:
            db.add(Line(**line_data.model_dump(), invoice_id=invoice.id))

        result.invoices_created += 1

    await db.commit()
    return result