# db/models/line.py
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Integer, DateTime, String, Numeric, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class Line(Base):
    __tablename__ = "lines"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    invoice_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("invoices.id"), nullable=True)
    quote_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("quotes.id"), nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    unit: Mapped[str | None] = mapped_column(String, nullable=True)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    discount_percent: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    # Relationships
    invoice: Mapped["Invoice"] = relationship(back_populates="lines")
    quote: Mapped["Quote"] = relationship(back_populates="lines")