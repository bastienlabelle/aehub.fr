from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, desc, func
from sqlalchemy.orm import selectinload
from datetime import date

from db.session import get_db
from db.models.payment import Payment
from db.models.invoice_payment import InvoicePayment
from db.models.user import User
from auth.dependencies import get_current_user
from schemas.payment import PaymentCreate, PaymentUpdate, PaymentResponse
from utils.invoice import recalculate_invoice_status

router = APIRouter(prefix="/payments", tags=["payments"])


async def generate_payment_number(user_id: int, db: AsyncSession) -> str:
    year = date.today().year
    result = await db.execute(
        select(func.max(Payment.number))
        .where(Payment.user_id == user_id, Payment.number.like(f"P{year}-%"))
    )
    last = result.scalar()
    counter = int(last.split("-")[1]) + 1 if last else 1
    return f"P{year}-{counter:03d}"


def payment_select(user_id: int):
    return (
        select(Payment)
        .where(Payment.user_id == user_id)
        .options(selectinload(Payment.invoices))
        .order_by(desc(Payment.number))

    )


@router.get("/next-number", response_model=dict)
async def next_payment_number(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return {"number": await generate_payment_number(current_user.id, db)}


@router.get("/", response_model=list[PaymentResponse])
async def list_payments(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(payment_select(current_user.id))
    return result.scalars().all()


@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_payment(
    payload: PaymentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    number = await generate_payment_number(current_user.id, db)
    payment = Payment(
        **payload.model_dump(exclude={"allocations"}),
        user_id=current_user.id,
        number=number,
    )
    db.add(payment)
    await db.flush()
    for alloc in payload.allocations:
        db.add(InvoicePayment(
            payment_id=payment.id,
            invoice_id=alloc.invoice_id,
            allocated_amount=alloc.allocated_amount,
        ))
    await db.flush()
    for alloc in payload.allocations:
        await recalculate_invoice_status(alloc.invoice_id, db)
    await db.commit()
    result = await db.execute(payment_select(current_user.id).where(Payment.id == payment.id))
    return result.scalar_one()


@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payment(
    payment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        payment_select(current_user.id).where(Payment.id == payment_id)
    )
    payment = result.scalar_one_or_none()
    if not payment:
        raise HTTPException(status_code=404, detail="Paiement introuvable")
    return payment


@router.patch("/{payment_id}", response_model=PaymentResponse)
async def update_payment(
    payment_id: int,
    payload: PaymentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        payment_select(current_user.id).where(Payment.id == payment_id)
    )
    payment = result.scalar_one_or_none()
    if not payment:
        raise HTTPException(status_code=404, detail="Paiement introuvable")

    old_invoice_ids = [ip.invoice_id for ip in payment.invoices]

    for key, value in payload.model_dump(exclude_unset=True, exclude={"allocations"}).items():
        setattr(payment, key, value)

    if payload.allocations is not None:
        await db.execute(delete(InvoicePayment).where(InvoicePayment.payment_id == payment.id))
        for alloc in payload.allocations:
            db.add(InvoicePayment(
                payment_id=payment.id,
                invoice_id=alloc.invoice_id,
                allocated_amount=alloc.allocated_amount,
            ))
        await db.flush()
        all_invoice_ids = set(old_invoice_ids) | {a.invoice_id for a in payload.allocations}
        for invoice_id in all_invoice_ids:
            await recalculate_invoice_status(invoice_id, db)

    await db.commit()
    result = await db.execute(payment_select(current_user.id).where(Payment.id == payment.id))
    return result.scalar_one()


@router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_payment(
    payment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        payment_select(current_user.id).where(Payment.id == payment_id)
    )
    payment = result.scalar_one_or_none()
    if not payment:
        raise HTTPException(status_code=404, detail="Paiement introuvable")

    invoice_ids = [ip.invoice_id for ip in payment.invoices]

    await db.delete(payment)
    await db.flush()

    for invoice_id in invoice_ids:
        await recalculate_invoice_status(invoice_id, db)

    await db.commit()