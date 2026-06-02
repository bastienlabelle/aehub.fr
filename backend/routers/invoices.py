from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, desc, func
from sqlalchemy.orm import selectinload
from datetime import date

from db.session import get_db
from db.models.invoice import Invoice
from db.models.invoice_payment import InvoicePayment
from db.models.line import Line
from db.models.user import User
from auth.dependencies import get_current_user
from schemas.invoice import InvoiceCreate, InvoiceUpdate, InvoiceResponse

router = APIRouter(prefix="/invoices", tags=["invoices"])


async def generate_invoice_number(user_id: int, db: AsyncSession) -> str:
    year = date.today().year
    result = await db.execute(
        select(func.max(Invoice.number))
        .where(Invoice.user_id == user_id, Invoice.number.like(f"F{year}-%"))
    )
    last = result.scalar()
    counter = int(last.split("-")[1]) + 1 if last else 1
    return f"F{year}-{counter:03d}"

def invoice_select(user_id: int):
    return (
        select(Invoice)
        .where(Invoice.user_id == user_id)
        .options(
            selectinload(Invoice.lines),
            selectinload(Invoice.client),
            selectinload(Invoice.payments).selectinload(InvoicePayment.payment),
        )
        .order_by(desc(Invoice.number))
    )


@router.get("/next-number", response_model=dict)
async def next_invoice_number(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return {"number": await generate_invoice_number(current_user.id, db)}


@router.get("/", response_model=list[InvoiceResponse])
async def list_invoices(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(invoice_select(current_user.id))
    return result.scalars().all()


@router.post("/", response_model=InvoiceResponse, status_code=status.HTTP_201_CREATED)
async def create_invoice(
    payload: InvoiceCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    number = await generate_invoice_number(current_user.id, db)
    invoice = Invoice(
        **payload.model_dump(exclude={"lines"}),
        user_id=current_user.id,
        number=number,
        status="draft",
    )
    db.add(invoice)
    await db.flush()
    for line_data in payload.lines:
        db.add(Line(**line_data.model_dump(), invoice_id=invoice.id))
    await db.commit()
    result = await db.execute(invoice_select(current_user.id).where(Invoice.id == invoice.id))
    return result.scalar_one()


@router.get("/{invoice_id}", response_model=InvoiceResponse)
async def get_invoice(
    invoice_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        invoice_select(current_user.id).where(Invoice.id == invoice_id)
    )
    invoice = result.scalar_one_or_none()
    if not invoice:
        raise HTTPException(status_code=404, detail="Facture introuvable")
    return invoice


@router.patch("/{invoice_id}", response_model=InvoiceResponse)
async def update_invoice(
    invoice_id: int,
    payload: InvoiceUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        invoice_select(current_user.id).where(Invoice.id == invoice_id)
    )
    invoice = result.scalar_one_or_none()
    if not invoice:
        raise HTTPException(status_code=404, detail="Facture introuvable")

    for key, value in payload.model_dump(exclude_unset=True, exclude={"lines"}).items():
        setattr(invoice, key, value)

    if payload.lines is not None:
        await db.execute(delete(Line).where(Line.invoice_id == invoice.id))
        for line_data in payload.lines:
            db.add(Line(**line_data.model_dump(), invoice_id=invoice.id))

    await db.commit()
    result = await db.execute(invoice_select(current_user.id).where(Invoice.id == invoice.id))
    return result.scalar_one()


@router.delete("/{invoice_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_invoice(
    invoice_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        invoice_select(current_user.id).where(Invoice.id == invoice_id)
    )
    invoice = result.scalar_one_or_none()
    if not invoice:
        raise HTTPException(status_code=404, detail="Facture introuvable")
    await db.delete(invoice)
    await db.commit()