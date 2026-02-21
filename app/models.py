from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import List
from enum import Enum
from datetime import datetime


class SourceSystem(str, Enum):
    partner_a = "partner_a"
    partner_b = "partner_b"
    internal = "internal"


class UserRecord(BaseModel):
    user_id: int = Field(gt=0)
    name: str = Field(min_length=3)
    email: EmailStr
    age: int = Field(ge=18, le=100)
    country: str
    signup_date: datetime
    is_active: bool

    @field_validator("country")
    @classmethod
    def normalize_country(cls, value):
        return value.upper()

    @field_validator("signup_date")
    @classmethod
    def validate_signup_date(cls, value):
        if value > datetime.utcnow():
            raise ValueError("Signup date cannot be in the future")
        return value


class IngestionRequest(BaseModel):
    batch_id: str
    source: SourceSystem
    records: List[UserRecord]


class IngestionResponse(BaseModel):
    batch_id: str
    total_records: int
    valid_records: int
    invalid_records: int
    errors: List[dict]