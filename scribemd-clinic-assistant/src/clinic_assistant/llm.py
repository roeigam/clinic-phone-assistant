from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Protocol, Any
import os
import json

class LLMProvider(Protocol):
    def extract(self, transcript: str) -> Optional[dict[str, Any]]:
        ...

@dataclass
class NoLLM:
    def extract(self, transcript: str) -> Optional[dict]:
        return None

@dataclass
class OpenAIChatCompletionsLLM:
    """
    Optional provider. Keep it off by default; enable via env var.
    This file is intentionally minimal; user can wire in their preferred SDK.
    """
    model: str = "gpt-4o-mini"  # example
    api_key_env: str = "OPENAI_API_KEY"

    def extract(self, transcript: str) -> Optional[dict]:
        api_key = os.getenv(self.api_key_env)
        if not api_key:
            return None

        # To keep dependencies minimal, we don't import openai here.
        # README will explain how to enable with preferred SDK.
        # Returning None forces heuristics.
        return None
