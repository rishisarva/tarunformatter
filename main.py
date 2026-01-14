import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

from config import BOT_TOKEN
from keyboards import main_menu, list_buttons
from filters import *
from image_sender import send_images
from state import *

PORT = int(os.environ.get("PORT", 10000))
WEBHOOK_URL = os.environ.get("RENDER_EXTERNAL_URL") + "/webhook"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    clear(update.effective_user.id)
    await update.message.reply_text("👕 Vision Jerseys", reply_markup=main_menu())


async def on_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id

    data = q.data

    if data == "menu:back":
        clear(uid)
        await q.message.edit_text("👕 Vision Jerseys", reply_markup=main_menu())
        return

    if data == "menu:clubs":
        await q.message.edit_text("Select Club", reply_markup=list_buttons(clubs(), "club"))
        return

    if data.startswith("club:"):
        club = data.split(":", 1)[1]
        await send_images(context.bot, q.message.chat_id, by_club(club))
        return

    if data == "menu:players":
        await q.message.edit_text("Select Player", reply_markup=list_buttons(players(), "player"))
        return

    if data.startswith("player:"):
        p = data.split(":", 1)[1]
        await send_images(context.bot, q.message.chat_id, by_player(p))
        return

    if data == "menu:random":
        all_imgs = []
        for v in TELEGRAM_FILE_MAP.values():
            all_imgs.extend(v)
        await send_images(context.bot, q.message.chat_id, all_imgs)
        return


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(on_callback))

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path="webhook",
        webhook_url=WEBHOOK_URL
    )


if __name__ == "__main__":
    main()