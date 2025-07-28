# Moops CRM Assistant — User Manual

**Demo:** [🚀 Launch Moops CRM on Hugging Face Spaces](https://huggingface.co/spaces/Siergej/Moops)  
**GitHub Repo:** [github.com/ssobol77/Moops](https://github.com/ssobol77/Moops)

---

<br>

## Overview

**Moops CRM Assistant** is an all-in-one AI-powered sales and customer communication tool.  
It enables managers to process merchandise/service orders through a chat interface, auto-log every order, send email notifications, and export data in multiple formats.

**Key Features:**
- Chatbot (LLM, Zephyr-7B) with FAQ awareness
- Quick auto-reply templates and customizable assistant strategy (system prompt)
- FAQ upload in Markdown (`*.md`) with instant context refresh
- SQLite order log with live database view from the UI
- Data export to JSON / CSV / Excel (XLSX) / SQLite
- Email notifications (Gmail SMTP) for managers and clients
- Manual “Notify manager” trigger
- One-file setup, deployable on Hugging Face Spaces, Render, Heroku, or your own server

---

<br>

## 1. Quick Start

### Requirements

- Python 3.10+ (Spaces use 3.10, local: 3.11+ recommended)
- All dependencies from `requirements.txt` (install with `uv pip install -r requirements.txt` or `pip install ...`)
- Environment variables: `HF_TOKEN`, `GMAIL_LOGIN`, `GMAIL_APP_PASS`, `MANAGER_EMAIL` (set in `.env` for local runs, via *Secrets* on Hugging Face Spaces)

### Launching

```bash
uv run app_all_in_one.py
````

The UI will be available at [http://127.0.0.1:7860](http://127.0.0.1:7860).

---

<br>

## 2. Interface Guide

| Element                 | Description                                                       |
| ----------------------- | ----------------------------------------------------------------- |
| **Client Email**        | *(Optional)* Customer email (used in notification emails).        |
| **Assistant Strategy**  | System prompt — sets the assistant’s persona and style.           |
| **Auto-reply Template** | One-click selection of a pre-made answer.                         |
| **Upload FAQ**          | Upload a Markdown `*.md` file with frequently asked questions.    |
| **FAQ Content**         | Displays current FAQ for reference and LLM context.               |
| **User Message**        | Field to input customer’s question or request.                    |
| **Chatbot**             | Main chat window; shows dialogue history (supports Markdown).     |
| **Reply & Save**        | Sends input to the LLM, saves the reply, and sends notifications. |
| **View DB**             | Displays the `orders` table (from `orders.db`) right in the UI.   |
| **Export**              | Buttons to export orders in JSON, CSV, XLSX, or flush to SQLite.  |
| **Notify manager**      | Sends a manual notification to the manager (no client involved).  |

---

<br>

## 3. Working with FAQ

1. Prepare a Markdown file, for example:

   ```markdown
   ## What is the minimum order?
   50 pieces.
   ```
2. Click **Upload FAQ** and select your file.
3. Click **Load FAQ** — FAQ content appears and is added to LLM context.
4. All chatbot answers will now incorporate this FAQ.

---

<br>

## 4. Data Export

| Button        | Output/Action                                                |
| ------------- | ------------------------------------------------------------ |
| **💾 JSON**   | Saves orders as `orders_YYYYMMDD_HHMMSS.json`.               |
| **📄 CSV**    | Spreadsheet-friendly format for Excel, LibreOffice, etc.     |
| **📗 XLSX**   | Exports as a native Excel file.                              |
| **📦 SQLite** | Flushes in-memory orders into the `orders.db` database file. |

---

<br>

## 5. Email Notifications

### Automatic

* Every **Reply & Save** triggers an email via Gmail SMTP to `MANAGER_EMAIL`.
* If *Client Email* is filled in, it can also notify the customer (configurable in `send_email_notification`).

### Manual

* Use the **Notify manager** button to manually send a message (for reminders, order processed, etc.).

---

<br>

## 6. Frequently Asked Questions (FAQ)

**Q:** Can I use a different language model?
**A:** Yes. Replace `InferenceClient("HuggingFaceH4/zephyr-7b-beta")` with your preferred checkpoint.

**Q:** Where are the exported files?
**A:** In the directory where you run the script.

**Q:** Can I deploy this on Render, Heroku, or Hugging Face Spaces?
**A:** Yes! Just provide required environment variables as *Secrets*.

**Q:** Is the chat history saved?
**A:** All interactions are logged to `orders.db` and can be exported.

---

<br>

## 7. Troubleshooting

If you run into problems:

* Ensure all dependencies from `requirements.txt` are installed.
* Check that all required environment variables are set (locally via `.env`, on Spaces via *Secrets*).
* Review terminal or Space logs for error messages.
* Restart the application after changing environment or configuration.
* Ensure your Python version is compatible (3.10+).
* For Gmail SMTP: enable App Passwords, use port 465, and ensure no 2FA blocks.
* For FAQ upload issues: check file encoding (UTF-8) and correct `.md` format.
* Data export errors: verify write permissions and active DB connection.
* To reset state: delete `orders.db` and restart the app (a new DB will be created).
* If the UI glitches, clear your browser cache or try another browser.
* For persistent issues, consult the community or open an issue on GitHub.
* See source code comments for customization hooks and further guidance.

---

<br>

## 8. Contributing & Support

* Issues and feature requests: [GitHub Issues](https://github.com/ssobol77/Moops/issues)
* For help, discussion, or to contribute: open a Pull Request or join the project discussions.
* Please follow standard open-source contribution guidelines.

---

<br>

## 9. Additional Resources

- [Hugging Face Documentation](https://huggingface.co/docs)
- [GitHub Pages Documentation](https://pages.github.com/)
- [Markdown Guide](https://www.markdownguide.org/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Python Documentation](https://docs.python.org/3/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Gmail API Documentation](https://developers.google.com/gmail/api)


---

<br>

## 10. License
This project is licensed under the MIT License. See the [LICENSE](https://github.com/ssobol77/Moops/blob/main/LICENSE) file for details.

---

<br>

*Last updated: 28.07.2025*


