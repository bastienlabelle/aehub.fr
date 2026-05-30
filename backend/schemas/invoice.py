from datetime import datetime, date
from pydantic import BaseModel
from schemas.line import LineCreate, LineResponse


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
    quote_id: int | None
    subject: str | None
    issued_at: date
    due_date: date | None
    status: str
    notes: str | None
    lines: list[LineResponse] = []
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}