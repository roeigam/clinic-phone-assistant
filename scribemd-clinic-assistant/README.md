# Clinic Phone Assistant (ScribeMD Exercise)

A simple AI-powered "clinic phone assistant" that takes a simulated call transcript and outputs structured JSON:
- intent classification
- structured extraction (name, DOB, callback number, reason/summary)
- urgency flagging

## How to run

```bash
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate
pip install -e .
echo "Hi, this is Sarah Cohen, born 03/12/1988. I need to book an appointment because I've had chest pain for two days. Please call me back at 310-555-2211." | clinic-assistant
