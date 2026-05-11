from pydantic import BaseModel, field_validator
from typing import Optional, Literal
from datetime import date
from decimal import Decimal
from src.utils.date_parser import parse_date
from src.utils.amount_parser import parse_amount

class BronzeOrder(BaseModel):
    model_config = {"str_strip_whitespace": True}

    order_id: str
    customer_id: str
    order_date: str
    amount: str
    payment_method: str
    status: str

class SilverOrder(BaseModel):
    model_config = {"str_strip_whitespace": True, "extra": "ignore"}

    order_id: str
    customer_id: str
    order_date: date
    amount: Optional[Decimal] = None
    payment_method: Literal["credit_card", "debit_card", "pix", "boleto"]
    status: Literal["paid", "completed", "refunded"]

    @field_validator("order_date", mode="before")
    @classmethod
    def validate_order_date(cls, v: str) -> str:
        try:
            parse_date(v)
            return v
        except ValueError:
            raise ValueError(f"order_date must be in the format 'YYYY-MM-DD', got '{v}'")

    @field_validator("amount", mode="before")
    @classmethod
    def validate_amount(cls, v: str) -> Optional[Decimal]:
        if v is None or v.strip() == "":
            return None
        try:
            return parse_amount(v)
        except ValueError:
            raise ValueError(f"amount must be a valid number, got '{v}'")


class GoldOrder(BaseModel):
    model_config = {"str_strip_whitespace": True, "extra": "ignore"}

    order_id: str
    customer_id: str
    order_date: date
    amount: Optional[Decimal] = None
    payment_method: str
    status: str
    processed_at: str