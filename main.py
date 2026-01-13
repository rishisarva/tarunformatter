# main.py

import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from config import BOT_TOKEN
from csv_loader import load_csv
from keyboards import main_menu, list_menu
from filters import *
from image_sender import send_images
from state import *


# ===============================
# 🔧 DUMMY HTTP SERVER (RENDER FIX)
# ===============================
def start_dummy_server():
    port = int(os.environ.get("PORT", 10000))

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Telegram bot is running")

        def log_message(self, format, *args):
            return

    HTTPServer(("0.0.0.0", port), Handler).serve_forever()


# ===============================
# /start COMMAND
# ===============================
async def start(update: Update, context):
    clear(update.effective_user.id)
    await update.message.reply_text(
        "Vision Jerseys 👕",
        reply_markup=main_menu()
    )


# ===============================
# TEXT / BUTTON HANDLER
# ===============================
async def handler(update: Update, context):
    text = update.message.text.lower()
    uid = update.message.from_user.id
    rows = load_csv()

    # Back
    if text == "⬅ back":
        clear(uid)
        await update.message.reply_text(
            "Main Menu",
            reply_markup=main_menu()
        )
        return

    # 🖼 CLUBS
    if text == "🖼 clubs":
        set(uid, "mode", "club")
        await update.message.reply_text(
            "Select Club",
            reply_markup=list_menu(clubs(rows))
        )
        return

    if get(uid, "mode") == "club":
        await send_images(
            context.bot,
            update.effective_chat.id,
            by_club(rows, text),
            text
        )
        clear(uid)
        return

    # 🖼 PLAYERS
    if text == "🖼 players":
        set(uid, "mode", "player")
        await update.message.reply_text(
            "Select Player",
            reply_markup=list_menu(players(rows)))
        return

    if get(uid, "mode") == "player":
        await send_images(
            context.bot,
            update.effective_chat.id,
            by_player(rows, text),
            text
        )
        clear(uid)
        return

    # 🎲 RANDOM
    if text == "🎲 random 15 jerseys":
        await send_images(
            context.bot,
            update.effective_chat.id,
            rows[:15],
            "random"
        )
        return


# ===============================
# 🚀 ENTRY POINT
# ===============================
def main():
    # Start Render dummy server
    threading.Thread(target=start_dummy_server, daemon=True).start()

    app = Application.builder().token(BOT_TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler))

    app.run_polling()


if __name__ == "__main__":
    main()