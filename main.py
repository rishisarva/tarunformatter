import asyncio
import os
from telegram import Update

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from config import BOT_TOKEN
from keyboards import main_menu, list_keyboard
from filters import *
from image_sender import send_images, send_whatsapp_random
from state import clear
from csv_loader import load_csv

PORT = int(os.environ.get("PORT", 10000))
WEBHOOK_URL = os.environ.get("RENDER_EXTERNAL_URL") + "/webhook"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    clear(update.effective_user.id)
    context.user_data.clear()
    await update.message.reply_text(
        "👕 Vision Jerseys",
        reply_markup=main_menu()
    )

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
async def self_ping(app):
    while True:
        try:
            await app.bot.get_me()
        except Exception:
            pass
        await asyncio.sleep(240)  # every 4 minutes
    # BACK
    if text == "⬅ back":
        context.user_data.clear()
        await update.message.reply_text("👕 Vision Jerseys", reply_markup=main_menu())
        return

    # MAIN MENU
    if text == "🖼 clubs":
        await update.message.reply_text("Select Club", reply_markup=list_keyboard(clubs()))
        context.user_data["mode"] = "club"
        return

    if text == "🖼 players":
        await update.message.reply_text("Select Player", reply_markup=list_keyboard(players()))
        context.user_data["mode"] = "player"
        return

    if text == "🖼 mix":
        context.user_data["mode"] = "mix_player"
        await update.message.reply_text("Select Player", reply_markup=list_keyboard(players()))
        return

    if text == "🖼 categories":
        context.user_data["mode"] = "category"
        await update.message.reply_text(
            "Select Sleeve Type",
            reply_markup=list_keyboard(categories())
        )
        return

    if text == "🎯 random technique":
        context.user_data["mode"] = "technique"
        await update.message.reply_text(
            "Select Technique",
            reply_markup=list_keyboard(techniques())
        )
        return

    if text == "🎲 random jerseys":
        imgs = []
        for v in TELEGRAM_FILE_MAP.values():
            imgs.extend(v)
        await send_images(context.bot, update.message.chat_id, imgs)
        return

    # ✅ WHATSAPP RANDOM 9 (CSV BASED)
    if text == "📲 whatsapp random 9":
        rows = load_csv()
        await send_whatsapp_random(
            context.bot,
            update.message.chat_id,
            rows
        )
        return

    # STATE HANDLING
    mode = context.user_data.get("mode")

    if mode == "club":
        await send_images(context.bot, update.message.chat_id, by_club(text))
        return

    if mode == "player":
        await send_images(context.bot, update.message.chat_id, by_player(text))
        return

    if mode == "category":
        await send_images(context.bot, update.message.chat_id, by_category(text))
        return

    if mode == "technique":
        await send_images(context.bot, update.message.chat_id, by_technique(text))
        return

    if mode == "mix_player":
        context.user_data["mix_player"] = text
        context.user_data["mode"] = "mix_club"
        await update.message.reply_text("Select Club", reply_markup=list_keyboard(clubs()))
        return

    if mode == "mix_club":
        player = context.user_data.get("mix_player")
        await send_images(
            context.bot,
            update.message.chat_id,
            by_player_club(player, text)
        )
        context.user_data.clear()
        return


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    # ✅ internal keep-alive (NO extra port)
    app.job_queue.run_once(
        lambda ctx: ctx.application.create_task(self_ping(ctx.application)),
        when=1
    )

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path="webhook",
        webhook_url=WEBHOOK_URL
    )

if __name__ == "__main__":
    main()