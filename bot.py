import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters


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
    token = os.environ.get("BOT_TOKEN")

    # 🔍 DEBUG (VERY IMPORTANT)
    print("BOT_TOKEN FOUND:", bool(token))
    if token:
        print("BOT_TOKEN LENGTH:", len(token))
    else:
        print("BOT_TOKEN IS NONE")

    if not token:
        # Do NOT crash Render
        print("Bot not started because BOT_TOKEN is missing.")
        while True:
            pass  # keep service alive so logs stay visible

    app = ApplicationBuilder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, format_text))

    print("Bot started successfully...")
    app.run_polling()


if __name__ == "__main__":
    main()
