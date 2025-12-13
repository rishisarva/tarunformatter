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
            # Lines without ":" → just remove stars
            new_line = line.replace("*", "").strip()

        if new_line:
            formatted_lines.append(f"• {new_line}")
        else:
            formatted_lines.append("")

    await update.message.reply_text("\n".join(formatted_lines))

app = ApplicationBuilder().token(os.environ["8529796522:AAG32rhrYwTK16RNF7Y_1mjLRQ-X_m5486U"]).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, format_text))
app.run_polling()
