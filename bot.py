import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters,
)

# ------------------ Flask dummy server (for Render FREE) ------------------
app_flask = Flask(__name__)

@app_flask.route("/")
def home():
    return "Bot is running", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port, use_reloader=False)

# ------------------ Telegram handlers ------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ Bot is active.\n\nSend your product description and I’ll format it."
    )

async def format_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    lines = text.split("\n")
    output = []

    for line in lines:
        raw = line.strip()

        if not raw:
            output.append("")
            continue

        # Remove existing bullets / dots / dashes
        while raw.startswith(("•", ".", "-", "·")):
            raw = raw[1:].strip()

        # Section headers (emoji + name, no colon)
        if ":" not in raw and "*" in raw:
            output.append(raw.replace("*", ""))
            continue

        # Key : Value lines
        if ":" in raw:
            left, right = raw.split(":", 1)
            left = left.replace("*", "").strip()
            output.append(f"• {left}: {right.strip()}")
            continue

        # Normal text
        output.append(raw.replace("*", ""))

    await update.message.reply_text("\n".join(output))


# ------------------ Main ------------------
def main():
    token = os.environ.get("BOT_TOKEN")

    if not token:
        print("BOT_TOKEN missing")
        return

    # Start Flask server in background (FREE Render requirement)
    threading.Thread(target=run_flask, daemon=True).start()

    tg_app = ApplicationBuilder().token(token).build()

    tg_app.add_handler(CommandHandler("start", start))
    tg_app.add_handler(MessageHandler(filter
