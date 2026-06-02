from pydantic import BaseModel
from decimal import Decimal
from datetime import date


class ImportLine(BaseModel):
    description: str
    quantity: Decimal
    unit: str | None = None
    unit_price: Decimal
    discount_percent: Decimal | None = None


class ImportInvoice(BaseModel):
    client_ref: str
    number: str
    subject: str | None = None
    issued_at: date
    due_date: date | None = None
    status: str = "draft"
    notes: str | None = None
    lines: list[ImportLine] = []


class ImportClient(BaseModel):
    name: str
    contact_name: str | None = None
    company_name: str | None = None
    email: str
    phone: str | None = None
    address: str | None = None
    zip_code: str | None = None
    city: str | None = None
    siren: str | None = None
    siret: str | None = None


class ImportAllocation(BaseModel):
    invoice_ref: str
    allocated_amount: Decimal


class ImportPayment(BaseModel):
    number: str
    paid_at: date
    amount: Decimal
    method: str | None = None
    reference: str | None = None
    notes: str | None = None
    allocations: list[ImportAllocation] = []


class ImportPayload(BaseModel):
    clients: list[ImportClient] = []
    invoices: list[ImportInvoice] = []
    payments: list[ImportPayment] = []


class ImportResult(BaseModel):
    clients_created: int
    clients_updated: int
    invoices_created: int
    invoices_skipped: int
    payments_created: int
    payments_skipped: int
    errors: list[str]