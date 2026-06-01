from datetime import datetime
from pydantic import BaseModel, EmailStr


class ClientCreate(BaseModel):
    name: str
    contact_name: str | None = None
    company_name: str | None = None
    email: EmailStr
    phone: str | None = None
    address: str | None = None
    zip_code: str | None = None
    city: str | None = None
    siret: str | None = None
    siren: str | None = None


class ClientUpdate(BaseModel):
    name: str
    contact_name: str | None = None
    company_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    address: str | None = None
    zip_code: str | None = None
    city: str | None = None
    siret: str | None = None
    siren: str | None = None


class ClientResponse(BaseModel):
    id: int
    user_id: int
    name: str | None = None
    contact_name: str | None = None
    company_name: str | None
    email: str
    phone: str | None
    address: str | None
    zip_code: str | None
    city: str | None
    siret: str | None
    siren: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}