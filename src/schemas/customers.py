from pydantic import BaseModel, field_validator
from typing import Optional, Literal
from datetime import datetime
from src.utils.date_parser import parse_date


class BronzeCustomer(BaseModel):
    model_config = {"str_strip_whitespace": True}

    customer_id: str
    cpf_hash: str
    name: str
    email: str
    phone: str
    city: str
    state: str
    created_at: str
    status: str


class SilverCustomer(BaseModel):
    model_config = {"str_strip_whitespace": True, "extra": "ignore"}

    customer_id: str
    cpf_hash: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    city: str
    state: str
    created_at: str
    status: Literal["active", "inactive", "blocked"]

    @field_validator("email", "phone", mode="before")
    @classmethod
    def empty_to_none(cls, v: str) -> Optional[str]:
        if v is not None and v.strip() == "":
            return None
        return v

    @field_validator("created_at", mode="before")
    @classmethod
    def validate_created_at(cls, v: str) -> str:
        try:
            parse_date(v)
            return v
        except ValueError:
            raise ValueError(
                f"created_at must be in the format 'YYYY-MM-DD', got '{v}'"
            )


class GoldCustomer(BaseModel):
    model_config = {"str_strip_whitespace": True, "extra": "ignore"}

    customer_id: str
    cpf_hash: str
    name_masked: str
    email_masked: Optional[str] = None
    phone_masked: Optional[str] = None
    city: str
    state: str
    created_at: str
    status: Literal["active", "inactive", "blocked"]
    processed_at: str
