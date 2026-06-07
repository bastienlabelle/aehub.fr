import csv
import io
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from datetime import date

from db.session import get_db
from db.models.payment import Payment
from db.models.invoice_payment import InvoicePayment
from db.models.invoice import Invoice
from db.models.user import User
from auth.dependencies import get_current_user

router = APIRouter(prefix="/accounting", tags=["accounting"])


@router.get("/livre-recettes")
async def livre_recettes(
    year: int = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if year is None:
        year = date.today().year

    result = await db.execute(
        select(Payment)
        .where(
            Payment.user_id == current_user.id,
            Payment.paid_at >= date(year, 1, 1),
            Payment.paid_at <= date(year, 12, 31),
        )
        .options(
            selectinload(Payment.invoices).selectinload(InvoicePayment.invoice).selectinload(Invoice.client)
        )
        .order_by(Payment.paid_at.asc())
    )
    payments = result.scalars().all()

    output = io.StringIO()
    writer = csv.writer(output, delimiter=';', quoting=csv.QUOTE_ALL)

    
    writer.writerow([
        "Date",
        "Numéro de facture",
        "Client",
        "Nature de la prestation",
        "Montant (€)",
        "Mode de paiement",
    ])

    for p in payments:
        # Résume les factures associées
        invoice_numbers = ", ".join(ip.invoice.number for ip in p.invoices if ip.invoice)
        client_names = ", ".join(
            dict.fromkeys(ip.invoice.client.name for ip in p.invoices if ip.invoice and ip.invoice.client)
        )
        subjects = ", ".join(
            dict.fromkeys(ip.invoice.subject for ip in p.invoices if ip.invoice and ip.invoice.subject)
        )

        writer.writerow([
            p.paid_at.strftime("%d/%m/%Y"),
            invoice_numbers or "—",
            client_names or "—",
            p.category or "-",
            f"{p.amount:.2f}".replace(".", ","),
            p.method or "—",
        ])

    output.seek(0)
    filename = f"livre-recettes-{year}.csv"

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )