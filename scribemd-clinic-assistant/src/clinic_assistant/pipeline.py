from __future__ import annotations
from typing import Optional
from .schema import CallResult
from .utils import normalize_text
from . import heuristics
from .llm import LLMProvider, NoLLM

def process_call(transcript: str, llm: Optional[LLMProvider] = None) -> CallResult:
    llm = llm or NoLLM()
    text = normalize_text(transcript)

    # 1) try LLM extraction (if configured)
    llm_data = llm.extract(text) or {}

    # 2) heuristics extraction fallback
    name = llm_data.get("name") or heuristics.extract_name(text)
    dob = llm_data.get("dob") or heuristics.extract_dob(text)
    phone = llm_data.get("phone") or heuristics.extract_phone(text)

    intent = llm_data.get("intent") or heuristics.classify_intent(text)
    summary = llm_data.get("summary") or heuristics.summarize_reason(text)
    urgency = llm_data.get("urgency") or heuristics.classify_urgency(text, intent)

    # normalize intent values a bit
    if intent not in CallResult.model_fields["intent"].annotation.__args__:
        intent = "other"

    if urgency not in ("low", "medium", "high"):
        urgency = "low"

    return CallResult(
        intent=intent,
        name=name,
        dob=dob,
        phone=phone,
        summary=summary,
        urgency=urgency,
    )
