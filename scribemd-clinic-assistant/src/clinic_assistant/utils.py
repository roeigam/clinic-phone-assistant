from __future__ import annotations
import re
from datetime import datetime

def normalize_text(t: str) -> str:
    # normalize whitespace, keep original punctuation mostly
    t = t.strip()
    t = re.sub(r"\s+", " ", t)
    return t

def to_iso_date(d: str) -> str | None:
    """
    Accepts common formats: MM/DD/YYYY, DD/MM/YYYY (ambiguous), YYYY-MM-DD.
    We assume US-style (MM/DD/YYYY) since example uses it; document in README.
    """
    d = d.strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", d):
        return d
    if re.fullmatch(r"\d{2}/\d{2}/\d{4}", d):
        mm, dd, yyyy = d.split("/")
        try:
            dt = datetime(int(yyyy), int(mm), int(dd))
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            return None
    return None

def clean_phone(p: str) -> str:
    return p.strip()
