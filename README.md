# AI Email Responder

**AI Email Responder** is a Streamlit-based application that uses OpenAI's GPT-4o-mini model to automatically generate professional email replies. It helps users save time, maintain a consistent tone, and improve productivity by drafting polite and context-aware responses.

---

## 🚀 Features

- Automatically generates **email subject and body** from raw email content.  
- Produces **structured JSON output** including:  
  - `reply_subject`  
  - `reply_body`  
  - `tone` (Formal | Friendly | Casual)  
  - `actions` (e.g., apologize, request info, escalate)  
- Copy-and-send ready email drafts.  
- Configurable OpenAI API key via Streamlit secrets or environment variables.  

---

## 🛠 Tech Stack

- **Frontend:** Streamlit  
- **Backend:** Python  
- **AI Model:** OpenAI GPT-4o-mini  
- **Key Modules:**  
  - `streamlit_app.py` – User interface and app flow  
  - `utils/llm_handler.py` – Handles OpenAI API calls  

---

## ⚡ Installation

1. Clone the repository:
```bash
git clone https://github.com/amarsin22/AI-Email-Responder1.git
cd AI-Email-Responder1
```

## 🏗 Workflow / Architecture

User Input → Streamlit UI → LLM Handler → OpenAI API → JSON Output → Display Draft

## 🧭 Architecture Diagram

![AI Email Responder Architecture](diagram(1).png)

