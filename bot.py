import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters


async def format_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    lines = text.split("\n")
    formatted_lines = []

    for line in lines:
        line = line.rstrip()

        # If line contains ":", clean only the LEFT side (label)
        if ":" in line:
            left, right = line.split(":", 1)
            left = left.replace("*", "").strip()
            new_line = f"{left} :{right}"
        else:
            # No ":" → remove stars safely
            new_line = line.replace("*", "").strip()

        # Add bullet only if line has content
        if new_line:
            formatted_lines.append(f"• {new_line}")
        else:
            formatted_lines.append("")

    await update.message.reply_text("\n".join(formatted_lines))


def main():
    token = os.environ.get("8529796522:AAG32rhrYwTK16RNF7Y_1mjLRQ-X_m5486U")
    if not token:
        raise RuntimeError("BOT_TOKEN environment variable not set")

    app = ApplicationBuilder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, format_text))

    print("Bot started successfully...")
    app.run_polling()


if __name__ == "__main__":
    main()
