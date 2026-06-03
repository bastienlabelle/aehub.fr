from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from datetime import date

from db.session import get_db
from db.models.invoice import Invoice
from db.models.client import Client
from db.models.quote import Quote
from db.models.line import Line
from db.models.payment import Payment
from db.models.user import User
from auth.dependencies import get_current_user

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/stats")
async def get_stats(
    year: int = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if year is None:
        year = date.today().year

    # CA encaissé cette année (basé sur payments)
    revenue_result = await db.execute(
        select(func.sum(Payment.amount))
        .where(
            Payment.user_id == current_user.id,
            Payment.paid_at >= date(year, 1, 1),
            Payment.paid_at <= date(year, 12, 31),
        )
    )
    revenue_paid = float(revenue_result.scalar() or 0)

    # CA en attente (factures sent + partial)
    pending_result = await db.execute(
        select(func.sum(
            Line.quantity * Line.unit_price * (1 - func.coalesce(Line.discount_percent, 0) / 100)
        ))
        .join(Invoice, Invoice.id == Line.invoice_id)
        .where(
            Invoice.user_id == current_user.id,
            Invoice.status.in_(['sent', 'partial']),
        )
    )
    revenue_pending = float(pending_result.scalar() or 0)

    # Nombre de clients
    clients_result = await db.execute(
        select(func.count(Client.id)).where(Client.user_id == current_user.id)
    )
    clients_count = clients_result.scalar() or 0

    # Devis en cours (draft + sent)
    quotes_result = await db.execute(
        select(func.count(Quote.id)).where(
            Quote.user_id == current_user.id,
            Quote.status.in_(['draft', 'sent']),
        )
    )
    quotes_count = quotes_result.scalar() or 0

    # CA mensuel basé sur payments
    monthly_result = await db.execute(
        select(
            func.extract('month', Payment.paid_at).label('month'),
            func.sum(Payment.amount).label('total')
        )
        .where(
            Payment.user_id == current_user.id,
            Payment.paid_at >= date(year, 1, 1),
            Payment.paid_at <= date(year, 12, 31),
        )
        .group_by(func.extract('month', Payment.paid_at))
        .order_by(func.extract('month', Payment.paid_at))
    )
    monthly_raw = monthly_result.all()
    monthly = [{"month": int(r.month), "total": float(r.total)} for r in monthly_raw]

    # Dernières factures (5)
    recent_result = await db.execute(
        select(Invoice)
        .where(Invoice.user_id == current_user.id)
        .options(selectinload(Invoice.client))
        .order_by(Invoice.issued_at.desc())
        .limit(5)
    )
    recent_invoices_raw = recent_result.scalars().all()

    # Factures en retard
    overdue_result = await db.execute(
        select(Invoice)
        .where(
            Invoice.user_id == current_user.id,
            Invoice.status.in_(['sent', 'partial']),
            Invoice.due_date < date.today(),
        )
        .options(selectinload(Invoice.client))
        .order_by(Invoice.due_date.asc())
    )
    overdue_raw = overdue_result.scalars().all()

    def format_invoice(inv):
        return {
            "id": inv.id,
            "number": inv.number,
            "client_name": inv.client.name,
            "issued_at": inv.issued_at.isoformat(),
            "due_date": inv.due_date.isoformat() if inv.due_date else None,
            "status": inv.status,
        }

    # Plus vieille année de paiement
    oldest_result = await db.execute(
        select(func.min(func.extract('year', Payment.paid_at)))
        .where(Payment.user_id == current_user.id)
    )
    oldest_year = int(oldest_result.scalar() or date.today().year)

    return {
        "revenue_paid": round(revenue_paid, 2),
        "revenue_pending": round(revenue_pending, 2),
        "clients_count": clients_count,
        "quotes_count": quotes_count,
        "monthly": monthly,
        "recent_invoices": [format_invoice(i) for i in recent_invoices_raw],
        "overdue_invoices": [format_invoice(i) for i in overdue_raw],
        "oldest_year": oldest_year,
    }

@router.get("/declarations")
async def get_declarations(
    year: int = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if year is None:
        year = date.today().year

    # CA par trimestre basé sur payments
    quarterly_result = await db.execute(
        select(
            func.extract('quarter', Payment.paid_at).label('quarter'),
            func.sum(Payment.amount).label('total')
        )
        .where(
            Payment.user_id == current_user.id,
            Payment.paid_at >= date(year, 1, 1),
            Payment.paid_at <= date(year, 12, 31),
        )
        .group_by(func.extract('quarter', Payment.paid_at))
        .order_by(func.extract('quarter', Payment.paid_at))
    )
    quarterly_raw = quarterly_result.all()
    quarterly = {int(r.quarter): round(float(r.total), 2) for r in quarterly_raw}

    # Plus vieille année de paiement
    oldest_result = await db.execute(
        select(func.min(func.extract('year', Payment.paid_at)))
        .where(Payment.user_id == current_user.id)
    )
    oldest_year = int(oldest_result.scalar() or year)

    return {
        "year": year,
        "oldest_year": oldest_year,
        "quarters": {
            "Q1": quarterly.get(1, 0),
            "Q2": quarterly.get(2, 0),
            "Q3": quarterly.get(3, 0),
            "Q4": quarterly.get(4, 0),
        }
    }