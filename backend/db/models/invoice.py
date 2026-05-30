# db/models/invoice.py
from datetime import datetime, date
from sqlalchemy import String, Integer, DateTime, Date, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class Invoice(Base):
    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    number: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    client_id: Mapped[int] = mapped_column(Integer, ForeignKey("clients.id"), nullable=False)
    quote_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("quotes.id"), nullable=True)
    subject: Mapped[str | None] = mapped_column(String, nullable=True)
    issued_at: Mapped[date] = mapped_column(Date, nullable=False)
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False, default="draft")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    # Relationships
    user: Mapped["User"] = relationship(back_populates="invoices")
    client: Mapped["Client"] = relationship(back_populates="invoices")
    quote: Mapped["Quote"] = relationship(back_populates="invoices")
    lines: Mapped[list["Line"]] = relationship("Line", back_populates="invoice", cascade="all, delete-orphan")
    payments: Mapped[list["InvoicePayment"]] = relationship(back_populates="invoice")