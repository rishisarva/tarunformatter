import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# ------------------ Flask dummy server ------------------
app_flask = Flask(__name__)

@app_flask.route("/")
def home():
    return "Bot is running", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)

# ------------------ Telegram bot ------------------
async def format_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    lines = text.split("\n")
    formatted_lines = []

    for line in lines:
        line = line.rstrip()

        if ":" in line:
            left, right = line.split(":", 1)
            left = left.replace("*", "").strip()
            new_line = f"{left} :{right}"
        else:
            new_line = line.replace("*", "").strip()

        if new_line:
            formatted_lines.append(f"• {new_line}")
        else:
            formatted_lines.append("")

    await update.message.reply_text("\n".join(formatted_lines))


def main():
    token = os.environ["BOT_TOKEN"]

    # Start Flask server in background
    threading.Thread(target=run_flask, daemon=True).start()

    tg_app = ApplicationBuilder().token(token).build()
    tg_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, format_text))

    print("Bot started successfully (FREE mode)...")
    tg_app.run_polling()


if __name__ == "__main__":
    main()