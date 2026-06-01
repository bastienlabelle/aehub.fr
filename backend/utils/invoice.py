from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from db.models.invoice import Invoice
from db.models.invoice_payment import InvoicePayment
from db.models.line import Line


async def recalculate_invoice_status(invoice_id: int, db: AsyncSession) -> None:
    # Total HT de la facture
    result = await db.execute(
        select(func.sum(
            Line.quantity * Line.unit_price * (1 - func.coalesce(Line.discount_percent, 0) / 100)
        )).where(Line.invoice_id == invoice_id)
    )
    total = result.scalar() or Decimal("0")

    # Total alloué
    result = await db.execute(
        select(func.sum(InvoicePayment.allocated_amount))
        .where(InvoicePayment.invoice_id == invoice_id)
    )
    allocated = result.scalar() or Decimal("0")

    # Mise à jour du statut
    result = await db.execute(select(Invoice).where(Invoice.id == invoice_id))
    invoice = result.scalar_one_or_none()
    if not invoice:
        return

    if allocated >= total:
        invoice.status = "paid"
    elif allocated > 0:
        invoice.status = "partial"
    # Si déjà draft ou sent, on ne rétrograde pas