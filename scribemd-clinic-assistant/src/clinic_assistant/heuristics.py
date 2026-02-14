from __future__ import annotations
import re
from typing import Optional, Tuple
from .utils import to_iso_date, clean_phone

NAME_PATTERNS = [
    # "this is Sarah Cohen"
    re.compile(r"\bthis is\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b", re.IGNORECASE),
    # "my name is Sarah Cohen"
    re.compile(r"\bmy name is\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b", re.IGNORECASE),
]

DOB_PATTERNS = [
    re.compile(r"\bborn\s+(\d{2}/\d{2}/\d{4})\b", re.IGNORECASE),
    re.compile(r"\bdob[:\s]+(\d{2}/\d{2}/\d{4})\b", re.IGNORECASE),
    re.compile(r"\bdate of birth[:\s]+(\d{2}/\d{2}/\d{4})\b", re.IGNORECASE),
    re.compile(r"\b(\d{4}-\d{2}-\d{2})\b"),
]

PHONE_PATTERNS = [
    re.compile(r"\b(\+?\d{1,2}[\s\-]?)?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{4}\b"),
    re.compile(r"\b\d{3}-\d{4}\b"),  # minimal local
]

INTENT_RULES = [
    ("urgent_medical_issue", [r"\bchest pain\b", r"\bshortness of breath\b", r"\bfaint(ed|ing)\b", r"\bstroke\b", r"\bsevere\b", r"\bunconscious\b", r"\bbleeding\b"]),
    ("appointment_booking", [r"\bbook\b.*\bappointment\b", r"\bschedule\b.*\bappointment\b", r"\bmake\b.*\bappointment\b", r"\bsee\b.*\bdoctor\b"]),
    ("prescription_refill", [r"\brefill\b", r"\bprescription\b", r"\bmeds?\b", r"\bpharmacy\b"]),
    ("billing_question", [r"\bbill\b", r"\bcharge\b", r"\binsurance\b", r"\bclaim\b", r"\bpayment\b"]),
]

URGENCY_HIGH = [r"\bchest pain\b", r"\btrouble breathing\b", r"\bshortness of breath\b", r"\bsuicid(al|e)\b", r"\bsevere\b", r"\bbleeding\b", r"\bpassed out\b", r"\bfaint(ed|ing)\b"]
URGENCY_MED = [r"\bfever\b", r"\bfor two days\b", r"\bfor 2 days\b", r"\bpain\b", r"\bworsening\b", r"\burgent\b"]

def extract_name(text: str) -> Optional[str]:
    for pat in NAME_PATTERNS:
        m = pat.search(text)
        if m:
            return " ".join(w.capitalize() for w in m.group(1).split())
    return None

def extract_dob(text: str) -> Optional[str]:
    for pat in DOB_PATTERNS:
        m = pat.search(text)
        if m:
            iso = to_iso_date(m.group(1))
            if iso:
                return iso
    return None

def extract_phone(text: str) -> Optional[str]:
    # Prefer "call me back at ..." if exists
    m = re.search(r"\bcall me back at\s+([0-9\-\+\(\)\s]{7,25})", text, re.IGNORECASE)
    if m:
        return clean_phone(m.group(1))
    for pat in PHONE_PATTERNS:
        m = pat.search(text)
        if m:
            return clean_phone(m.group(0))
    return None

def classify_intent(text: str) -> str:
    low = text.lower()
    for intent, patterns in INTENT_RULES:
        for p in patterns:
            if re.search(p, low):
                return intent
    return "general_question"

def classify_urgency(text: str, intent: str) -> str:
    low = text.lower()
    if intent == "urgent_medical_issue":
        return "high"
    for p in URGENCY_HIGH:
        if re.search(p, low):
            return "high"
    for p in URGENCY_MED:
        if re.search(p, low):
            return "medium"
    return "low"

def summarize_reason(text: str) -> str:
    # naive summarization: strip identity lines, keep main request clause
    t = text
    t = re.sub(r"\b(this is|my name is)\b.*?(?=[\.\,]|$)", "", t, flags=re.IGNORECASE)
    t = re.sub(r"\bborn\s+\d{2}/\d{2}/\d{4}\b", "", t, flags=re.IGNORECASE)
    t = re.sub(r"\bcall me back at\b.*?(?=[\.\,]|$)", "", t, flags=re.IGNORECASE)
    t = re.sub(r"\s+", " ", t).strip(" ,.")
    # keep short
    return t[:240] if len(t) > 240 else t
