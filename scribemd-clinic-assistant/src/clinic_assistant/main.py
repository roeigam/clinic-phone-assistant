from __future__ import annotations
import json
import sys
from .pipeline import process_call

def app():
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        print("Usage: clinic-assistant [TRANSCRIPT]\nIf no transcript arg is given, reads from stdin.")
        raise SystemExit(0)

    if len(sys.argv) > 1:
        transcript = " ".join(sys.argv[1:])
    else:
        transcript = sys.stdin.read()

    result = process_call(transcript)
    print(json.dumps(result.model_dump(), indent=2, ensure_ascii=False))
