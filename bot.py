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

# ------------------ Flask dummy server (Render FREE) ------------------
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
        raw = line.rstrip()

        # Empty line → keep spacing
        if not raw.strip():
            output.append("")
            continue

        # 🔥 REMOVE ALL leading bullets, dots, dashes, spaces, tabs
        cleaned = raw.lstrip(" •.-·\t")

        # 🔹 Section headers (emoji + name, no colon)
        if ":" not in cleaned and "*" in cleaned:
            output.append(cleaned.replace("*", ""))
            continue

        # 🔹 Key : Value lines
        if ":" in cleaned:
            left, right = cleaned.split(":", 1)
            left = left.replace("*", "").strip()
            output.append(f"• {left}: {right.strip()}")
            continue

        # 🔹 Normal text (intro / footer)
        output.append(cleaned.replace("*", ""))

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
    tg_app.add_handler(MessageHandler(filters.TEXT, format_text))

    print("Bot started successfully and listening for messages...")
    tg_app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
