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

from config import BOT_TOKEN, TELEGRAM_FILE_MAP
from keyboards import main_menu, list_menu
from filters import clubs, players, by_club, by_player, smart
from image_sender import send_images
from state import set, get, clear

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
    text = update.message.text.lower()
    uid = update.message.from_user.id

    # BACK
    if text == "⬅ back":
        clear(uid)
        await update.message.reply_text("Main Menu", reply_markup=main_menu())
        return

    # CLUBS
    if text == "🖼 clubs":
        set(uid, "mode", "club")
        await update.message.reply_text(
            "Select Club",
            reply_markup=list_menu(clubs())
        )
        return

   if get(uid, "mode") == "club":
    images = by_club(text)

    if not images:
        await update.message.reply_text(
            "❌ No jerseys found for this club.\nTry another.",
            reply_markup=list_menu(clubs())
        )
        return

    await send_images(
        context.bot,
        update.effective_chat.id,
        images
    )

    clear(uid)
    return
    # PLAYERS
    if text == "🖼 players":
        set(uid, "mode", "player")
        await update.message.reply_text(
            "Select Player",
            reply_markup=list_menu(players())
        )
        return

    if get(uid, "mode") == "player":
        await send_images(
            context.bot,
            update.effective_chat.id,
            by_player(text)
        )
        clear(uid)
        return

    # SMART
    if text == "🧠 smart club / player":
        set(uid, "mode", "smart")
        await update.message.reply_text("Type club or player name")
        return

    if get(uid, "mode") == "smart":
        images = smart(club=text) + smart(player=text)
        await send_images(
            context.bot,
            update.effective_chat.id,
            images
        )
        clear(uid)
        return

    # RANDOM
    if text == "🎲 random 15 jerseys":
        all_imgs = []
        for imgs in TELEGRAM_FILE_MAP.values():
            all_imgs.extend(imgs)

        await send_images(
            context.bot,
            update.effective_chat.id,
            all_imgs
        )
        return


# ===============================
# ENTRY
# ===============================
def main():
    threading.Thread(target=start_dummy_server, daemon=True).start()

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler))

    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()