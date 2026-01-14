# main.py
import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config import BOT_TOKEN, TELEGRAM_FILE_MAP
from keyboards import main_menu, list_menu
from filters import *
from image_sender import send_images
from state import *

PORT = int(os.environ.get("PORT", 10000))
WEBHOOK_URL = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/webhook"


# ===============================
# /start
# ===============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    clear(update.effective_user.id)
    await update.message.reply_text(
        "👕 Vision Jerseys",
        reply_markup=main_menu()
    )


# ===============================
# MESSAGE HANDLER
# ===============================
async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    uid = update.effective_user.id

    # BACK
    if text == "⬅ back":
        clear(uid)
        await update.message.reply_text("Main Menu", reply_markup=main_menu())
        return

    # CLUBS
    if text == "🖼 clubs":
        set(uid, "mode", "club")
        await update.message.reply_text("Select Club", reply_markup=list_menu(clubs()))
        return

    if get(uid, "mode") == "club":
        await send_images(context.bot, update.effective_chat.id, by_club(text))
        return  # ❗ DO NOT clear mode → allows repeat

    # PLAYERS
    if text == "🖼 players":
        set(uid, "mode", "player")
        await update.message.reply_text("Select Player", reply_markup=list_menu(players()))
        return

    if get(uid, "mode") == "player":
        await send_images(context.bot, update.effective_chat.id, by_player(text))
        return

    # SMART
    if text == "🧠 smart club / player":
        set(uid, "mode", "smart")
        await update.message.reply_text("Type club or player name")
        return

    if get(uid, "mode") == "smart":
        images = smart(club=text) + smart(player=text)
        await send_images(context.bot, update.effective_chat.id, images)
        return

    # RANDOM
    if text == "🎲 random 15 jerseys":
        all_imgs = []
        for imgs in TELEGRAM_FILE_MAP.values():
            all_imgs.extend(imgs)

        await send_images(context.bot, update.effective_chat.id, all_imgs[:15])
        return


# ===============================
# WEBHOOK ENTRY
# ===============================
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler))

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL,
        url_path="webhook",
    )


if __name__ == "__main__":
    main()