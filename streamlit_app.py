# streamlit_app.py
import streamlit as st
from utils.llm_handler import call_llm_generate_reply
from utils.email_utils import build_incoming_email_text, parse_json_safe, simple_signature
import json

st.set_page_config(page_title="AI Email Responder", page_icon="✉️", layout="centered")

st.title("✉️ AI Email Responder")
st.markdown(
    "Paste or upload an incoming email and generate a professional reply draft using OpenAI. "
    "Use **Test Mode** if you don't have an API key yet."
)

st.sidebar.header("Settings")
use_test_mode = st.sidebar.checkbox("Test Mode (no API call)", value=False)
model_choice = st.sidebar.selectbox("Model", ["gpt-4o-mini", "gpt-3.5-turbo"], index=0)

if st.sidebar.checkbox("Enter API key manually (for testing)"):
    dev_api_key = st.sidebar.text_input("API Key", type="password")
else:
    dev_api_key = None

st.subheader("Incoming Email")
subject = st.text_input("Subject", "Order #1234 refund request")
from_addr = st.text_input("From", "rachel@gmail.com")
body = st.text_area("Body", "Hi team,\n\nI was charged for order #1234 although it was cancelled.\nPlease refund.\n\nThanks,\nRachel")

tone_pref = st.selectbox("Preferred Tone", ["Formal", "Friendly", "Casual"], index=0)
include_signature = st.checkbox("Include signature", value=True)
signature_name = st.text_input("Signature name", value="Customer Support")

if st.button("Generate Reply"):
    incoming_text = build_incoming_email_text(subject, from_addr, body)

    if use_test_mode:
        st.warning("Test Mode enabled — no real API call.")
        raw_output = json.dumps({
            "reply_subject": f"Re: {subject}",
            "reply_body": f"Hi Rachel,\n\nThanks for your message. I’ve initiated the refund for order #1234. You’ll receive confirmation within 3–5 business days.{simple_signature(signature_name)}",
            "tone": tone_pref,
            "actions": ["refund_initiated"]
        }, indent=2)
    else:
        try:
            raw_output = call_llm_generate_reply(incoming_text, api_key=dev_api_key, model=model_choice)
        except Exception as e:
            st.error(f"LLM call failed: {e}")
            raw_output = None

    if raw_output:
        with st.expander("📋 Raw Output"):
            st.code(raw_output, language="json")

        try:
            parsed = parse_json_safe(raw_output)
            reply_subject = parsed.get("reply_subject", f"Re: {subject}")
            reply_body = parsed.get("reply_body", "")

            if include_signature and signature_name not in reply_body:
                reply_body += simple_signature(signature_name)

            st.subheader("✍️ Generated Reply")
            edited_reply = st.text_area("Edit before sending", value=reply_body, height=220)
            st.text_input("Reply Subject", value=reply_subject, key="subject_field")

            if st.button("Send Reply (Simulate)"):
                st.success("✅ Reply sent successfully (simulated).")
        except Exception as e:
            st.error(f"Could not parse output: {e}")
