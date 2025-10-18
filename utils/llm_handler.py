import streamlit as st
from openai import OpenAI

def get_api_key():
    try:
        return st.secrets["OPENAI_API_KEY"]
    except Exception:
        return None

API_KEY = get_api_key()

def init_client(api_key=None):
    key = api_key or API_KEY
    if not key:
        raise ValueError("OpenAI API key not provided. Set .streamlit/secrets.toml or pass api_key.")
    return OpenAI(api_key=key)

SYSTEM_PROMPT = """
You are a professional email assistant. Given the raw incoming email (including sender, subject, and body),
generate a polite, concise, and context-appropriate reply draft. Output JSON with keys:
{
  "reply_subject": "...",
  "reply_body": "Full message body with greeting and signature.",
  "tone": "Formal | Friendly | Casual",
  "actions": ["what the reply will do e.g., apologize, request info, escalate"]
}
Return ONLY valid JSON (no extra text or markdown). If any field cannot be determined, return null for it.
Be concise and helpful.
"""

def call_llm_generate_reply(incoming_email_text: str, api_key: str | None = None, model: str = "gpt-4o-mini"):
    client = init_client(api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Incoming email:\n{incoming_email_text}\n\nReturn only JSON."}
        ],
        temperature=0.1,
        max_tokens=600,
    )
    return response.choices[0].message.content.strip()
