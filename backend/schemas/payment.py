from datetime import datetime, date
from decimal import Decimal
from pydantic import BaseModel


class InvoiceAllocationCreate(BaseModel):
    invoice_id: int
    allocated_amount: Decimal


class InvoiceAllocationResponse(BaseModel):
    id: int
    invoice_id: int
    allocated_amount: Decimal

    model_config = {"from_attributes": True}


class PaymentCreate(BaseModel):
    paid_at: date
    amount: Decimal
    method: str | None = None
    reference: str | None = None
    notes: str | None = None
    allocations: list[InvoiceAllocationCreate] = []


class PaymentUpdate(BaseModel):
    paid_at: date | None = None
    amount: Decimal | None = None
    method: str | None = None
    reference: str | None = None
    notes: str | None = None
    allocations: list[InvoiceAllocationCreate] | None = None


class PaymentResponse(BaseModel):
    id: int
    user_id: int
    number: str
    paid_at: date
    amount: Decimal
    method: str | None
    reference: str | None
    notes: str | None
    allocations: list[InvoiceAllocationResponse] = []
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}