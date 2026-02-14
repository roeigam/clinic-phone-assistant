from clinic_assistant.pipeline import process_call

def test_example_urgent():
    inp = "Hi, this is Sarah Cohen, born 03/12/1988. I need to book an appointment because I've had chest pain for two days. Please call me back at 310-555-2211."
    out = process_call(inp).model_dump()
    assert out["name"] == "Sarah Cohen"
    assert out["dob"] == "1988-03-12"
    assert out["phone"] == "310-555-2211"
    assert out["intent"] in ("urgent_medical_issue", "appointment_booking")  # rules may choose urgent
    assert out["urgency"] in ("high", "medium")
