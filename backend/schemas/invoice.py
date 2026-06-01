from datetime import datetime, date
from decimal import Decimal
from pydantic import BaseModel, model_validator
from schemas.line import LineCreate, LineResponse
from schemas.client import ClientResponse


class InvoicePaymentInfo(BaseModel):
    id: int
    payment_id: int
    allocated_amount: Decimal
    payment_number: str | None = None
    paid_at: date | None = None
    method: str | None = None

    model_config = {"from_attributes": True}

    @model_validator(mode='before')
    @classmethod
    def extract_payment_fields(cls, v: any) -> any:
        if hasattr(v, 'payment') and v.payment:
            v.__dict__['payment_number'] = v.payment.number
            v.__dict__['paid_at'] = v.payment.paid_at
            v.__dict__['method'] = v.payment.method
        return v


class InvoiceCreate(BaseModel):
    client_id: int
    quote_id: int | None = None
    subject: str | None = None
    issued_at: date
    due_date: date | None = None
    notes: str | None = None
    lines: list[LineCreate] = []


class InvoiceUpdate(BaseModel):
    client_id: int | None = None
    subject: str | None = None
    issued_at: date | None = None
    due_date: date | None = None
    status: str | None = None
    notes: str | None = None
    lines: list[LineCreate] | None = None


class InvoiceResponse(BaseModel):
    id: int
    user_id: int
    number: str
    client_id: int
    client: ClientResponse
    quote_id: int | None
    subject: str | None
    issued_at: date
    due_date: date | None
    status: str
    notes: str | None
    lines: list[LineResponse] = []
    payments: list[InvoicePaymentInfo] = []
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}