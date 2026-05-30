from decimal import Decimal
from pydantic import BaseModel


class LineCreate(BaseModel):
    description: str
    quantity: Decimal
    unit: str | None = None
    unit_price: Decimal
    discount_percent: Decimal | None = None


class LineResponse(BaseModel):
    id: int
    description: str
    quantity: Decimal
    unit: str | None
    unit_price: Decimal
    discount_percent: Decimal | None

    model_config = {"from_attributes": True}