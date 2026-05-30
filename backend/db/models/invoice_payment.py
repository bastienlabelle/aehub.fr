# db/models/invoice_payment.py
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Integer, DateTime, Numeric, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class InvoicePayment(Base):
    __tablename__ = "invoices_payments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    invoice_id: Mapped[int] = mapped_column(Integer, ForeignKey("invoices.id"), nullable=False)
    payment_id: Mapped[int] = mapped_column(Integer, ForeignKey("payments.id"), nullable=False)
    allocated_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    # Relationships
    invoice: Mapped["Invoice"] = relationship(back_populates="payments")
    payment: Mapped["Payment"] = relationship(back_populates="invoices")