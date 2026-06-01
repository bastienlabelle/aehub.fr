from datetime import datetime, date
from decimal import Decimal
from pydantic import BaseModel
from schemas.line import LineCreate, LineResponse
from schemas.client import ClientResponse


class QuoteCreate(BaseModel):
    client_id: int
    subject: str | None = None
    issued_at: date
    valid_until: date | None = None
    notes: str | None = None
    lines: list[LineCreate] = []


class QuoteUpdate(BaseModel):
    client_id: int | None = None
    subject: str | None = None
    issued_at: date | None = None
    valid_until: date | None = None
    status: str | None = None
    notes: str | None = None
    lines: list[LineCreate] | None = None  # None = ne pas toucher, [] = tout supprimer


class QuoteResponse(BaseModel):
    id: int
    user_id: int
    number: str
    client: ClientResponse  # remplace client_id
    subject: str | None
    issued_at: date
    valid_until: date | None
    status: str
    notes: str | None
    lines: list[LineResponse] = []
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}