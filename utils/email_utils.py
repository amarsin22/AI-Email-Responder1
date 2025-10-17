# utils/email_utils.py
import re
import json

def build_incoming_email_text(subject: str, from_addr: str, body: str) -> str:
    """Compose a single text blob to feed to the model."""
    template = f"From: {from_addr}\nSubject: {subject}\n\n{body}"
    return template

def extract_json_obj(raw_output: str):
    """Extract the first {...} JSON substring from LLM output (robust to extra text)."""
    match = re.search(r"\{[\s\S]*\}", raw_output)
    if not match:
        raise ValueError("No JSON object found in model output.")
    return match.group()

def parse_json_safe(raw_output: str):
    """Return dict parsed from raw_output (attempt to extract JSON then parse)."""
    try:
        jstr = extract_json_obj(raw_output)
        return json.loads(jstr)
    except Exception as e:
        raise ValueError(f"Failed to parse JSON from LLM output: {e}")

def simple_signature(name="Support Team"):
    return f"\n\nBest regards,\n{name}"
