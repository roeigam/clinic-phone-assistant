from __future__ import annotations
from pydantic import BaseModel, Field, field_validator
from typing import Literal, Optional
import re
from datetime import date

Intent = Literal[
    "appointment_booking",
    "prescription_refill",
    "billing_question",
    "urgent_medical_issue",
    "general_question",
    "other",
]

Urgency = Literal["low", "medium", "high"]

class CallResult(BaseModel):
    intent: Intent
    name: Optional[str] = None
    dob: Optional[str] = Field(default=None, description="YYYY-MM-DD")
    phone: Optional[str] = None
    summary: str
    urgency: Urgency

    @field_validator("phone")
    @classmethod
    def phone_format(cls, v):
        if v is None:
            return v
        # allow digits, spaces, dashes, parentheses, plus
        if not re.fullmatch(r"[0-9\-\+\(\)\s]{7,25}", v):
            raise ValueError("phone appears invalid")
        return v

    @field_validator("dob")
    @classmethod
    def dob_format(cls, v):
        if v is None:
            return v
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", v):
            raise ValueError("dob must be YYYY-MM-DD")
        # basic calendar validity
        y, m, d = map(int, v.split("-"))
        date(y, m, d)
        return v
