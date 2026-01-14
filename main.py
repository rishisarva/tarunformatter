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

from config import BOT_TOKEN, TELEGRAM_FILE_MAP
from keyboards import main_menu, list_menu
from filters import *
from image_sender import send_images
from state import *

print("Loaded clubs:", len(TELEGRAM_FILE_MAP))


# ===============================
# RENDER DUMMY SERVER
# ===============================
def start_dummy_server():
    port = int(os.environ.get("PORT", 10000))

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot running")

        def log_message(self, *args):
            return

    HTTPServer(("0.0.0.0", port), Handler).serve_forever()


# ===============================
# /start
# ===============================
async def start(update: Update, context):
    clear(update.effective_user.id)
    await update.message.reply_text(
        "👕 Vision Jerseys",
        reply_markup=main_menu()
    )


# ===============================
# MESSAGE HANDLER
# ===============================
async def handler(update: Update, context):
    text = update.message.text.lower().strip()
    uid = update.effective_user.id
    chat_id = update.effective_chat.id

    # BACK
    if text == "⬅ back":
        clear(uid)
        await update.message.reply_text("Main Menu", reply_markup=main_menu())
        return

    # MENU BUTTONS
    if text == "🖼 clubs":
        set(uid, "mode", "club")
        await update.message.reply_text(
            "Select Club",
            reply_markup=list_menu(clubs())
        )
        return

    if text == "🖼 players":
        set(uid, "mode", "player")
        await update.message.reply_text(
            "Select Player",
            reply_markup=list_menu(players())
        )
        return

    if text == "🧠 smart club / player":
        set(uid, "mode", "smart")
        await update.message.reply_text("Type club or player name")
        return

    # 🔥 DIRECT CLUB MATCH (REPEATABLE)
    if text in TELEGRAM_FILE_MAP:
        await send_images(
            context.bot,
            chat_id,
            TELEGRAM_FILE_MAP[text]
        )
        return

    # MODE HANDLING
    mode = get(uid, "mode")

    if mode == "club":
        await send_images(context.bot, chat_id, by_club(text))
        return

    if mode == "player":
        await send_images(context.bot, chat_id, by_player(text))
        return

    if mode == "smart":
        images = smart(club=text) + smart(player=text)
        await send_images(context.bot, chat_id, images)
        return

    # RANDOM
    if text == "🎲 random 15 jerseys":
        all_imgs = []
        for imgs in TELEGRAM_FILE_MAP.values():
            all_imgs.extend(imgs)

        await send_images(context.bot, chat_id, all_imgs[:15])
        return

    # FALLBACK
    await update.message.reply_text(
        "❓ Please use menu buttons",
        reply_markup=main_menu()
    )


# ===============================
# ENTRY
# ===============================
def main():
    threading.Thread(target=start_dummy_server, daemon=True).start()

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler))

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()