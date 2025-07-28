# 🛍️ Moops CRM Assistant - All‑in‑One

<br>

A full-featured **Gradio-based CRM web application** powered by Zephyr-7B LLM, Markdown FAQ integration, SQLite order logging, multiple data export formats, and built-in email notifications.

> 🚀 **[View Live Demo on Hugging Face Spaces](https://huggingface.co/spaces/Siergej/Moops)**  
> 🌐 **[GitHub Repository](https://github.com/ssobol77/Moops)**

---

<br>

## ✅ Key Features

| Category           | Description |
|--------------------|-------------|
| 🤖 LLM Assistant   | Uses **Zephyr-7B** via HuggingFace with streaming support |
| 🧠 Customizable Prompt | Flexible “Assistant Strategy” and pre-built auto-reply templates |
| 📄 FAQ Integration | Upload any `.md` FAQ or use the built-in file — FAQ content is always included in LLM context |
| 🗄️ Order Logging   | Orders are saved to **SQLite (`orders.db`)**; browse directly in the UI |
| 💾 Data Export     | Export orders to **JSON, CSV, XLSX** or flush memory log to SQLite with one click |
| ✉️ Email Notifications | Manager notified automatically (Gmail SMTP); optional client copy; "Notify manager" button |
| 🖥️ Modern UI      | Built on Gradio 4, mobile-friendly, with Markdown rendering in chat |

---

<br>

## 📦 Requirements

- **Python 3.11+** (recommended: 3.11 or 3.12)
- [`uv`](https://github.com/astral-sh/uv) for fast package management (or use `pip`)

```bash
uv pip install -r requirements.txt
````

---

<br>

## 🔐 Environment Variables

Create a `.env` file in your project root (do **not** commit to public repositories):

```ini
HF_TOKEN=hf_XXXXXXXXXXXXXXXXXXXXXXXXXXXX
GMAIL_LOGIN=your_gmail@gmail.com
GMAIL_APP_PASS=16_char_app_password
MANAGER_EMAIL=manager@example.com
```

> **Hugging Face Spaces:** Use Settings ➜ Secrets instead of a file.

---

<br>

## 🚀 Running Locally

```bash
uv run app_all_in_one.py
```

The app will launch at **[http://localhost:7860](http://localhost:7860)**.

---

<br>

## 📤 Deploying to Hugging Face Spaces

1. Fork or clone this repo, then push to your Space:

   ```bash
   git remote set-url origin https://<USERNAME>:<HF_TOKEN>@huggingface.co/spaces/<USERNAME>/Moops
   git add .
   git commit -m "🚀 Initial release"
   git push origin main
   ```
2. Set your environment variables (Settings ➜ Secrets).
3. The Space will build and show the Gradio app automatically.

---

<br>

## 🗂️ Project Layout

```
.
├── app.py        # Main Gradio application
├── faq.md                   # Default FAQ (Markdown)
├── orders.db                # SQLite database (auto-created)
├── requirements.txt         # Python dependencies
└── README.md                # This document
```

---

<br>

## 💡 User Manual

### Interface Overview

| Element                 | Description                                            |
| ----------------------- | ------------------------------------------------------ |
| **Client Email**        | (Optional) Customer's email for notifications          |
| **Assistant Strategy**  | System prompt to define assistant’s persona and style  |
| **Auto-reply Template** | Quick selection of a prebuilt reply template           |
| **Upload FAQ**          | Upload a Markdown `.md` file with your FAQ             |
| **FAQ Content**         | Shows the current FAQ — always included in LLM context |
| **User Message**        | Enter customer queries or requests here                |
| **Chatbot**             | Dialogue window (supports Markdown rendering)          |
| **Reply & Save**        | Sends to LLM, saves to log, sends notifications        |
| **View DB**             | Browse the `orders` table (from `orders.db`) in the UI |
| **Export**              | Export orders as JSON / CSV / XLSX / flush to SQLite   |
| **Notify manager**      | Manual email to manager (no client email required)     |

---

<br>

### Data Export

| Button              | Action                                              |
| ------------------- | --------------------------------------------------- |
| **Export JSON**     | Download orders as JSON                             |
| **Export CSV**      | Download orders as CSV (Excel/LibreOffice)          |
| **Export XLSX**     | Download orders as Excel spreadsheet                |
| **Flush to SQLite** | Save in-memory log to SQLite database (`orders.db`) |
| **View DB**         | View the SQLite `orders` table directly in the UI   |

---

<br>

### Email Notifications

* **Automatic**: Every order sends an email to the manager (and optionally to the client, if email provided).
* **Manual**: "Notify manager" button sends a custom message to the manager’s email.

---

<br>
### FAQ Workflow

1. Prepare your FAQ as a Markdown file (e.g.):

   ```markdown
   ## What is the minimum order?
   50 pieces.
   ```
2. Use **Upload FAQ** to load it into the app.
3. Click **Load uploaded FAQ** — the text will appear in the FAQ Content field.
4. The FAQ is now always included in the system prompt for every reply.

---

<br>

### Troubleshooting

If you encounter issues, check the following:

* Are all dependencies installed?
* Are environment variables correctly set?
* Check logs for error messages.
* Is your model compatible?
* Restart the app after configuration changes.
* For errors, check your Python version and package versions.
* Email not working? Check Gmail/SMTP settings and credentials.
* FAQ not loading? Validate your Markdown file.
* Export failing? Check database connection and directory permissions.
* To reset: delete `orders.db` and restart the app.
* UI issues? Clear browser cache or try a different browser.
* Update dependencies after pulling changes: `uv pip install -r requirements.txt`.
* For more tips, see the [User Manual](#user-manual).

---

<br>

## 📚 Frequently Asked Questions (FAQ)

* **Q:** *Can I use a different LLM/model?*
  **A:** Yes! Change the model name in `app_all_in_one.py` as needed.
* **Q:** *How do I customize auto-reply templates?*
  **A:** Edit `app_all_in_one.py` (see `auto_templates` dict).
* **Q:** *How do I reset or backup the database?*
  **A:** Just copy or remove `orders.db` — it’s auto-created on next run.
* **Q:** *Where are my exported files?*
  **A:** In your project directory (where the script runs).
* **Q:** *How do I contribute or report bugs?*
  **A:** Open an issue or PR on [GitHub](https://github.com/ssobol77/Moops).
* **Q:** *Can I deploy to Heroku/Render/Cloud?*
  **A:** Yes. Make sure to set env variables (`HF_TOKEN`, etc.) and check storage.
* **Q:** *How do I change the port?*
  **A:** Set `server_port` in `demo.launch()` in the main app file.
* **Q:** *Is there a mobile app?*
  **A:** No, but the Gradio UI works on mobile browsers.

---

<br>

## 🪪 License

MIT License.

---

> For help or feedback, open an issue on [GitHub](https://github.com/ssobol77/Moops) or visit the [Hugging Face Space](https://huggingface.co/spaces/Siergej/Moops).

> Happy CRM managing! 🎉
````
