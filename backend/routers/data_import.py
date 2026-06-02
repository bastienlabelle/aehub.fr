from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from db.session import get_db
from db.models.client import Client
from db.models.invoice import Invoice
from db.models.invoice_payment import InvoicePayment
from db.models.line import Line
from db.models.payment import Payment
from db.models.user import User
from auth.dependencies import get_current_user
from schemas.data_import import ImportPayload, ImportResult
from utils.invoice import recalculate_invoice_status

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
        payments_created=0,
        payments_skipped=0,
        errors=[],
    )

    # Map email -> client_id
    client_map: dict[str, int] = {}

    # Import clients
    for c in payload.clients:
        # Nettoyage
        if c.siret:
            c.siret = c.siret.replace(' ', '')
        if c.siren:
            c.siren = c.siren.replace(' ', '')
        if c.phone:
            c.phone = c.phone.replace(' ', '')
        if c.zip_code:
            c.zip_code = c.zip_code.replace(' ', '')
        # Si name pas fourni, on le construit
        if not c.name:
            c.name = c.company_name or c.contact_name or c.email
        if not c.company_name:
            c.company_name = c.name

        existing = await db.execute(
            select(Client).where(
                Client.email == c.email,
                Client.user_id == current_user.id
            )
        )
        client = existing.scalar_one_or_none()

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

    # Map numéro -> invoice_id
    invoice_map: dict[str, int] = {}

    # Import invoices
    for inv in payload.invoices:
        existing = await db.execute(
            select(Invoice).where(
                Invoice.number == inv.number,
                Invoice.user_id == current_user.id
            )
        )
        existing_inv = existing.scalar_one_or_none()
        if existing_inv:
            result.invoices_skipped += 1
            result.errors.append(f"Facture {inv.number} déjà existante, ignorée")
            invoice_map[inv.number] = existing_inv.id
            continue

        client_id = client_map.get(inv.client_ref)
        if not client_id:
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

        await db.flush()
        invoice_map[inv.number] = invoice.id
        result.invoices_created += 1

    # Import payments
    for p in payload.payments:
        existing = await db.execute(
            select(Payment).where(
                Payment.number == p.number,
                Payment.user_id == current_user.id
            )
        )
        if existing.scalar_one_or_none():
            result.payments_skipped += 1
            result.errors.append(f"Paiement {p.number} déjà existant, ignoré")
            continue

        payment = Payment(
            user_id=current_user.id,
            number=p.number,
            paid_at=p.paid_at,
            amount=p.amount,
            method=p.method,
            reference=p.reference,
            notes=p.notes,
        )
        db.add(payment)
        await db.flush()

        for alloc in p.allocations:
            invoice_id = invoice_map.get(alloc.invoice_ref)
            if not invoice_id:
                existing_inv = await db.execute(
                    select(Invoice).where(
                        Invoice.number == alloc.invoice_ref,
                        Invoice.user_id == current_user.id
                    )
                )
                inv_obj = existing_inv.scalar_one_or_none()
                if not inv_obj:
                    result.errors.append(f"Facture '{alloc.invoice_ref}' introuvable pour le paiement {p.number}")
                    continue
                invoice_id = inv_obj.id
                invoice_map[alloc.invoice_ref] = invoice_id

            db.add(InvoicePayment(
                payment_id=payment.id,
                invoice_id=invoice_id,
                allocated_amount=alloc.allocated_amount,
            ))

        await db.flush()

        for alloc in p.allocations:
            inv_id = invoice_map.get(alloc.invoice_ref)
            if inv_id:
                await recalculate_invoice_status(inv_id, db)

        result.payments_created += 1

    await db.commit()
    return result