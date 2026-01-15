import os
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

from config import BOT_TOKEN
from keyboards import main_menu, list_buttons
from filters import *
from image_sender import send_images
from state import clear

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

    # -------- CLUBS --------
    if data == "menu:clubs":
        await q.message.edit_text("Select Club", reply_markup=list_buttons(clubs(), "club"))
        return

    if data.startswith("club:"):
        await send_images(context.bot, q.message.chat_id, by_club(data.split(":",1)[1]))
        return

    # -------- PLAYERS --------
    if data == "menu:players":
        await q.message.edit_text("Select Player", reply_markup=list_buttons(players(), "player"))
        return

    if data.startswith("player:"):
        await send_images(context.bot, q.message.chat_id, by_player(data.split(":",1)[1]))
        return

    # -------- MIX --------
if data == "menu:mix":
    context.user_data["mix"] = {}
    await q.message.edit_text("Select Player", reply_markup=list_buttons(players(), "mixp"))
    return

if data.startswith("mixp:"):
    context.user_data.setdefault("mix", {})
    context.user_data["mix"]["player"] = data.split(":",1)[1]
    await q.message.edit_text("Select Club", reply_markup=list_buttons(clubs(), "mixc"))
    return

if data.startswith("mixc:"):
    mix = context.user_data.get("mix")
    if not mix:
        await q.message.reply_text("⚠️ Please start mix again")
        return

    p = mix["player"]
    c = data.split(":",1)[1]

    await send_images(
        context.bot,
        q.message.chat_id,
        by_player_club(p, c)
    )

    context.user_data.clear()
    return
    # -------- CATEGORY --------
    if data == "menu:categories":
        await q.message.edit_text("Select Sleeve Type", reply_markup=list_buttons(categories(), "cat"))
        return

    if data.startswith("cat:"):
        await send_images(context.bot, q.message.chat_id, by_category(data.split(":",1)[1]))
        return

    # -------- TECHNIQUE --------
    if data == "menu:technique":
        await q.message.edit_text("Select Technique", reply_markup=list_buttons(techniques(), "tech"))
        return

    if data.startswith("tech:"):
        await send_images(context.bot, q.message.chat_id, by_technique(data.split(":",1)[1]))
        return

    # -------- RANDOM --------
    if data == "menu:random":
        imgs = []
        for v in TELEGRAM_FILE_MAP.values():
            imgs.extend(v)
        await send_images(context.bot, q.message.chat_id, imgs)
        return

    # -------- WHATSAPP 9 --------
    if data == "menu:wa9":
        imgs = []
        for v in TELEGRAM_FILE_MAP.values():
            imgs.extend(v)

        await send_images(
            context.bot,
            q.message.chat_id,
            imgs,
            caption=(
                "👕 Premium Football Jerseys\n\n"
                "📏 Sizes: S • M • L • XL • XXL\n\n"
                "🔗 https://visionsjersey.com\n\n"
                "✨ Limited stock — order now!"
            )
        )
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