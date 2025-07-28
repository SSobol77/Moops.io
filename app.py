"""
app.py — Moops CRM Assistant
---------------------------------------

A full‑featured CRM web application (Gradio 5.x):

* LLM (HuggingFace Zephyr‑7B) with streaming
* Auto‑reply templates + configurable system‑prompt
* Markdown‑FAQ loading (default `faq.md`)
* SQLite order log (`orders.db`) with in‑UI viewer
* Order export → JSON / CSV / SQLite / XLSX
* Email notifications (Gmail SMTP) for client and/or manager
* Manual “Notify manager” button
"""

from __future__ import annotations

import csv
import datetime
import json
import os
import sqlite3
import smtplib
from email.message import EmailMessage
from pathlib import Path
from typing import List, Dict

import gradio as gr
import pandas as pd
from dotenv import load_dotenv, find_dotenv
from huggingface_hub import InferenceClient


# ───────────────────────────────────────────────
# Email helpers (credentials come from .env)
# ───────────────────────────────────────────────

# Load .env (the first file found, or explicit path)
load_dotenv(find_dotenv(filename=".env", raise_error_if_not_found=False))

# Read environment variables
MANAGER_EMAIL  = os.getenv("MANAGER_EMAIL")
GMAIL_LOGIN    = os.getenv("GMAIL_LOGIN")
GMAIL_APP_PASS = os.getenv("GMAIL_APP_PASS")

# Fail fast if any creds are missing
missing = [name for name, val in {
    "MANAGER_EMAIL": MANAGER_EMAIL,
    "GMAIL_LOGIN":   GMAIL_LOGIN,
    "GMAIL_APP_PASS": GMAIL_APP_PASS,
}.items() if not val]

if missing:
    raise RuntimeError(
        f"Missing email credentials in .env: {', '.join(missing)}.\n"
        "Create a .env file with:\n"
        "MANAGER_EMAIL=manager@example.com\n"
        "GMAIL_LOGIN=your_gmail@gmail.com\n"
        "GMAIL_APP_PASS=app_password_16_chars"
    )

def send_email_notification(subject: str, body: str, to_email: str | None = None) -> None:
    """Send an email via Gmail SMTP (SSL, port 465)."""
    msg            = EmailMessage()
    msg["From"]    = GMAIL_LOGIN
    msg["To"]      = to_email or MANAGER_EMAIL
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(GMAIL_LOGIN, GMAIL_APP_PASS)
        smtp.send_message(msg)

def send_notification_to_manager(subject: str, body: str) -> None:
    """Shortcut → always deliver to MANAGER_EMAIL."""
    send_email_notification(subject, body, MANAGER_EMAIL)


# ──────────────────────────────────────────
# Constants and Hugging Face client
# ──────────────────────────────────────────
DB_FILE          = "orders.db"
FAQ_DEFAULT_PATH = "faq.md"
orders_log: List[Dict] = []

auto_templates = {
    "Greeting":            "Hello! 👋 Welcome to our service. How can I assist you today?",
    "Pricing Info":        "Our base pricing starts from **$10 per item**, with a minimum order of "
                           "**50 units**. Discounts apply for larger orders. Would you like a quote?",
    "Thank you":           "Thank you for reaching out. We look forward to helping you. Have a great day!",
    "Custom T-shirt Quote": "Sure! Please provide the number of shirts and colors in the design and "
                            "we’ll send you a detailed quote."
}

HF_TOKEN = os.getenv("HF_TOKEN")
client   = InferenceClient("HuggingFaceH4/zephyr-7b-beta", token=HF_TOKEN)

# ──────────────────────────────────────────
#  SQLite initialization
# ──────────────────────────────────────────
def init_db() -> None:
    conn = sqlite3.connect(DB_FILE)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            email TEXT,
            user TEXT,
            assistant TEXT
        )
        """
    )
    conn.close()

init_db()

# ──────────────────────────────────────────
# FAQ helpers
# ──────────────────────────────────────────
def load_faq_text(md_file) -> str:
    if md_file is None:
        return "No FAQ file uploaded."
    return Path(md_file.name).read_text(encoding="utf-8")

def load_default_faq() -> str:
    p = Path(FAQ_DEFAULT_PATH)
    return p.read_text(encoding="utf-8") if p.exists() else ""

# ──────────────────────────────────────────
#  Export helpers
# ──────────────────────────────────────────
def save_to_json() -> str:
    fname = f"orders_{datetime.datetime.now():%Y%m%d_%H%M%S}.json"
    Path(fname).write_text(json.dumps(orders_log, ensure_ascii=False, indent=2), encoding="utf-8")
    return f"✅ Saved {fname}"

def export_to_csv() -> str:
    fname = f"orders_{datetime.datetime.now():%Y%m%d_%H%M%S}.csv"
    with open(fname, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "email", "user", "assistant"])
        writer.writeheader()
        writer.writerows(orders_log)
    return f"📄 Saved {fname}"

def export_to_sqlite() -> str:
    conn = sqlite3.connect(DB_FILE)
    with conn:
        for row in orders_log:
            conn.execute(
                "INSERT INTO orders (timestamp, email, user, assistant) VALUES (?, ?, ?, ?)",
                (row["timestamp"], row["email"], row["user"], row["assistant"]),
            )
    return f"📦 Flushed to {DB_FILE}"

def export_to_xlsx() -> str:
    conn = sqlite3.connect(DB_FILE)
    df   = pd.read_sql_query("SELECT * FROM orders ORDER BY id", conn)
    conn.close()
    fname = f"orders_{datetime.datetime.now():%Y%m%d_%H%M%S}.xlsx"
    df.to_excel(fname, index=False)
    return f"📗 Saved {fname}"

# ──────────────────────────────────────────
# View DB helper
# ──────────────────────────────────────────
def view_db_contents() -> str:
    conn = sqlite3.connect(DB_FILE)
    df   = pd.read_sql_query("SELECT * FROM orders ORDER BY id DESC", conn)
    conn.close()
    return df.to_markdown(index=False)

# ──────────────────────────────────────────
#  Main respond function
# ──────────────────────────────────────────
def respond(
    message: str,
    history: list[dict] | None,
    email: str,
    strategy_text: str,
    template_choice: str,
    faq_content: str,
    max_tokens: int,
    temperature: float,
    top_p: float,
):
    """
    Generate assistant reply, log the order, send notifications.

    Returns
    -------
    (updated_history, gr.update(""))  -> clears the input box.
    """
    system_message = strategy_text.strip() or "You are a helpful assistant."
    if faq_content:
        system_message += f"\n\nAdditional info from FAQ:\n{faq_content.strip()}"
    if template_choice:
        system_message += f"\n\n[Template]: {auto_templates.get(template_choice, template_choice)}"

    messages = [{"role": "system", "content": system_message}]
    if history:
        messages.extend(m for m in history if m["role"] in ("user", "assistant"))

    messages.append({"role": "user", "content": message})

    partial_reply   = ""
    visual_history  = history or []
    visual_history += [{"role": "user", "content": message}]

    for chunk in client.chat_completion(
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        stream=True,
    ):
        delta = chunk.choices[0].delta.content or ""
        partial_reply += delta
        yield visual_history + [{"role": "assistant", "content": partial_reply}], gr.update(value="")

    # Finalize the history
    final_history = visual_history + [{"role": "assistant", "content": partial_reply}]

    # Store order
    order_row = {
        "timestamp": datetime.datetime.now().isoformat(),
        "email": email,
        "user": message,
        "assistant": partial_reply,
    }
    orders_log.append(order_row)

    conn = sqlite3.connect(DB_FILE)
    with conn:
        conn.execute(
            "INSERT INTO orders (timestamp, email, user, assistant) VALUES (?, ?, ?, ?)",
            (order_row["timestamp"], email, message, partial_reply),
        )

    # Email manager/client
    try:
        subj = f"📩 New CRM interaction from {email or 'anonymous'}"
        body = (
            f"Customer:\n{message}\n\nAssistant:\n{partial_reply}\n\n"
            f"Strategy:\n{strategy_text}\nTemplate:\n{template_choice}"
        )
        send_email_notification(subj, body)
    except Exception as exc:
        print(f"❌ Email send failed: {exc}")

    yield final_history, gr.update(value="")

# ──────────────────────────────────────────
#  Manual manager notification
# ──────────────────────────────────────────
def notify_manager_click() -> str:
    subj = "📬 Manual Moops CRM Notification"
    msg  = f"Manual trigger at {datetime.datetime.now():%Y-%m-%d %H:%M:%S}"
    try:
        send_notification_to_manager(subj, msg)
        return "📧 Manager notified."
    except Exception as exc:
        return f"❌ Notification failed: {exc}"

# ──────────────────────────────────────────
#  Gradio UI
# ──────────────────────────────────────────
with gr.Blocks(title="Moops CRM All‑in‑One") as demo:
    gr.Markdown("# 🛍️ Moops CRM Assistant — All‑in‑One")

    # Input controls
    with gr.Row():
        client_email   = gr.Textbox(label="Client Email", placeholder="client@example.com")
        strategy_text  = gr.Textbox(label="Assistant Strategy", value="You are a polite business assistant...")

    template_choice = gr.Radio(list(auto_templates.keys()), value="Greeting", label="📋 Auto‑reply Template")

    with gr.Row():
        faq_upload  = gr.File(label="📄 Upload FAQ (Markdown)", file_types=[".md"])
        faq_textbox = gr.Textbox(label="FAQ Content", lines=10, value=load_default_faq())

    gr.Button("📂 Load uploaded FAQ").click(load_faq_text, faq_upload, faq_textbox)

    # Chat interface
    chatbot    = gr.Chatbot(render_markdown=True, type="messages", label="💬 Chatbot")
    user_input = gr.Textbox(label="💬 User Message")

    with gr.Row():
        max_tokens  = gr.Slider(1, 4096, value=1024, label="Max tokens")
        temperature = gr.Slider(0.1, 4.0, value=0.7, step=0.1, label="Temperature")
        top_p       = gr.Slider(0.1, 1.0, value=0.95, step=0.05, label="Top‑p")

    template_choice.change(lambda t: auto_templates[t], template_choice, user_input)

    user_input.submit(
        respond,
        [user_input, chatbot, client_email, strategy_text, template_choice, faq_textbox,
         max_tokens, temperature, top_p],
        [chatbot, user_input],
    )

    # Export/DB/Notification controls
    gr.Markdown("### 💾 Export")
    gr.Button("💾 JSON").click(lambda: save_to_json(), None, gr.Textbox(lines=1))
    gr.Button("📄 CSV").click(lambda: export_to_csv(), None, gr.Textbox(lines=1))
    gr.Button("📦 Flush to SQLite").click(lambda: export_to_sqlite(), None, gr.Textbox(lines=1))
    gr.Button("📗 XLSX").click(lambda: export_to_xlsx(), None, gr.Textbox(lines=1))

    gr.Markdown("### 📊 View DB")
    gr.Button("🔍 View orders.db").click(lambda: view_db_contents(), None, gr.Textbox(lines=15))

    gr.Markdown("### 📫 Notify")
    gr.Button("📩 Notify manager").click(lambda: notify_manager_click(), None, gr.Textbox(lines=1))

if __name__ == "__main__":
    demo.launch()

