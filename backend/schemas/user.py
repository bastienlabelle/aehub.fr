from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    company_name: str | None = None
    first_name: str
    last_name: str
    siren: str
    siret: str
    address: str
    zip_code: str
    city: str
    phone: str | None = None
    email: EmailStr
    website: str | None = None
    iban: str | None = None
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    company_name: str | None
    first_name: str
    last_name: str
    siren: str
    siret: str
    address: str
    zip_code: str
    city: str
    phone: str | None
    email: str
    website: str | None
    iban: str | None
    invoice_counter: int
    quote_counter: int
    payment_counter: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class UserUpdate(BaseModel):
    company_name: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    siren: str | None = None
    siret: str | None = None
    address: str | None = None
    zip_code: str | None = None
    city: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    website: str | None = None
    iban: str | None = None
    password: str | None = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"