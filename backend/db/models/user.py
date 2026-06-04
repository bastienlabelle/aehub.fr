# db/models/user.py
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, LargeBinary, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    company_name: Mapped[str | None] = mapped_column(String, nullable=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    siren: Mapped[str] = mapped_column(String(9), nullable=False)
    siret: Mapped[str] = mapped_column(String(14), nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=False)
    zip_code: Mapped[str] = mapped_column(String, nullable=False)
    city: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[str | None] = mapped_column(String, nullable=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    website: Mapped[str | None] = mapped_column(String, nullable=True)
    iban: Mapped[str | None] = mapped_column(String, nullable=True)
    password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    invoice_counter: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    quote_counter: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    payment_counter: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    invoice_template: Mapped[str] = mapped_column(String, nullable=False, default="default", server_default="default")

    # Relationships
    clients: Mapped[list["Client"]] = relationship(back_populates="user")
    invoices: Mapped[list["Invoice"]] = relationship(back_populates="user")
    quotes: Mapped[list["Quote"]] = relationship(back_populates="user")
    payments: Mapped[list["Payment"]] = relationship(back_populates="user")