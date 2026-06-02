from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, desc, func
from sqlalchemy.orm import selectinload
from datetime import date

from db.session import get_db
from db.models.quote import Quote
from db.models.line import Line
from db.models.user import User
from auth.dependencies import get_current_user
from schemas.quote import QuoteCreate, QuoteUpdate, QuoteResponse

router = APIRouter(prefix="/quotes", tags=["quotes"])


def generate_quote_number(counter: int) -> str:
    from datetime import date
    year = date.today().year
    return f"D{year}-{counter:03d}"


def quote_select(user_id: int):
    return (
        select(Quote)
        .where(Quote.user_id == user_id)
        .options(
            selectinload(Quote.lines),
            selectinload(Quote.client),
        )
        .order_by(desc(Quote.number))

    )


@router.get("/next-number", response_model=dict)
async def next_quote_number(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    year = date.today().year
    result = await db.execute(
        select(func.max(Quote.number))
        .where(Quote.user_id == current_user.id, Quote.number.like(f"D{year}-%"))
    )
    last = result.scalar()
    counter = int(last.split("-")[1]) + 1 if last else 1
    return {"number": f"D{year}-{counter:03d}"}

@router.get("/", response_model=list[QuoteResponse])
async def list_quotes(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(quote_select(current_user.id))
    return result.scalars().all()


@router.post("/", response_model=QuoteResponse, status_code=status.HTTP_201_CREATED)
async def create_quote(
    payload: QuoteCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    current_user.quote_counter += 1
    number = generate_quote_number(current_user.quote_counter)
    quote = Quote(
        **payload.model_dump(exclude={"lines"}),
        user_id=current_user.id,
        number=number,
        status="draft",
    )
    db.add(quote)
    await db.flush()
    for line_data in payload.lines:
        db.add(Line(**line_data.model_dump(), quote_id=quote.id))
    await db.commit()
    result = await db.execute(quote_select(current_user.id).where(Quote.id == quote.id))
    return result.scalar_one()


@router.get("/{quote_id}", response_model=QuoteResponse)
async def get_quote(
    quote_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        quote_select(current_user.id).where(Quote.id == quote_id)
    )
    quote = result.scalar_one_or_none()
    if not quote:
        raise HTTPException(status_code=404, detail="Devis introuvable")
    return quote


@router.patch("/{quote_id}", response_model=QuoteResponse)
async def update_quote(
    quote_id: int,
    payload: QuoteUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        quote_select(current_user.id).where(Quote.id == quote_id)
    )
    quote = result.scalar_one_or_none()
    if not quote:
        raise HTTPException(status_code=404, detail="Devis introuvable")

    for key, value in payload.model_dump(exclude_unset=True, exclude={"lines"}).items():
        setattr(quote, key, value)

    if payload.lines is not None:
        await db.execute(delete(Line).where(Line.quote_id == quote.id))
        for line_data in payload.lines:
            db.add(Line(**line_data.model_dump(), quote_id=quote.id))

    await db.commit()
    result = await db.execute(quote_select(current_user.id).where(Quote.id == quote.id))
    return result.scalar_one()


@router.delete("/{quote_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_quote(
    quote_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        quote_select(current_user.id).where(Quote.id == quote_id)
    )
    quote = result.scalar_one_or_none()
    if not quote:
        raise HTTPException(status_code=404, detail="Devis introuvable")
    await db.delete(quote)
    await db.commit()