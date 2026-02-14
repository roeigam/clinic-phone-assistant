# Clinic Phone Assistant (ScribeMD Technical Exercise)

A simple “clinic phone assistant” that takes a simulated phone call transcript (text) and returns **clean structured JSON**:
- intent classification (appointment / prescription / billing / urgent / etc.)
- extraction of key patient info (name, date of birth, callback number, reason)
- urgency flagging

The focus is on **reasoning, structure, and practical AI integration**, not UI polish.

---

## Features

- **Input:** free-form call transcript (single text string)
- **Output:** validated JSON with:
  - `intent`
  - `name`
  - `dob` (ISO format: `YYYY-MM-DD`)
  - `phone`
  - `summary` (reason for call)
  - `urgency` (`low` / `medium` / `high`)
- Deterministic baseline (regex + rules) that works out-of-the-box
- Optional hook for LLM provider (interface included; can be wired easily)

---

## Project Structure

