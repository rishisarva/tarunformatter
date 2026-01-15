from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from keyboards import main_menu, list_menu
from filters import *
from image_sender import send_album
from config import BOT_TOKEN, WEBHOOK_URL, WEBHOOK_PATH
import random

# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "👕 Vision Jerseys",
        reply_markup=main_menu()
    )

# ---------------- BUTTONS ----------------
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()  # IMPORTANT for repeat clicks
    data = q.data
    chat_id = q.message.chat_id

    # ---------- CLUBS ----------
    if data == "clubs":
        await q.message.edit_text(
            "Select Club",
            reply_markup=list_menu(clubs(), "club")
        )

    elif data.startswith("club:"):
        club = data.split(":", 1)[1]
        await send_album(
            context.bot,
            chat_id,
            by_club(club)
        )

    # ---------- CATEGORIES (SLEEVES) ----------
    elif data == "categories":
        await q.message.edit_text(
            "Select Sleeve Type",
            reply_markup=list_menu(
                ["short sleeve", "full sleeve", "polo"],
                "cat"
            )
        )

    elif data.startswith("cat:"):
        sleeve = data.split(":", 1)[1]
        await send_album(
            context.bot,
            chat_id,
            by_category(sleeve)
        )

    # ---------- SMART SEARCH ----------
    elif data == "smart":
        context.user_data["smart"] = True
        await q.message.reply_text(
            "Type *club or player name* 👇",
            parse_mode="Markdown"
        )

    # ---------- RANDOM 9 (NORMAL) ----------
    elif data == "random":
        all_imgs = []
        for v in TELEGRAM_FILE_MAP.values():
            all_imgs.extend(v)

        random.shuffle(all_imgs)

        await send_album(
            context.bot,
            chat_id,
            all_imgs[:9]
        )

    # ---------- WHATSAPP POST (RANDOM 9) ----------
    elif data == "wa_post":
        all_imgs = []
        for v in TELEGRAM_FILE_MAP.values():
            all_imgs.extend(v)

        random.shuffle(all_imgs)

        await send_album(
            context.bot,
            chat_id,
            all_imgs[:9],
            caption=(
                "👕 Premium Football Jerseys Available\n\n"
                "📏 Sizes: S • M • L • XL • XXL\n\n"
                "🔗 https://visionsjersey.com\n\n"
                "✨ Limited stock — order yours today!"
            )
        )

# ---------------- TEXT HANDLER ----------------
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("smart"):
        imgs = smart_search(update.message.text)

        await send_album(
            context.bot,
            update.message.chat_id,
            imgs,
            caption=(
                "👕 Jersey Available\n\n"
                "📏 Sizes: S • M • L • XL • XXL\n\n"
                "🔗 https://visionsjersey.com\n\n"
                "💬 Tap the link & order now"
            )
        )

        context.user_data.clear()
        return

    # fallback
    await update.message.reply_text(
        "Use the menu below 👇",
        reply_markup=main_menu()
    )

# ---------------- MAIN ----------------
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", start))
    app.add_handler(CommandHandler("restart", start))

    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler)
    )

    app.run_webhook(
        listen="0.0.0.0",
        port=10000,
        webhook_url=WEBHOOK_URL,
        url_path=WEBHOOK_PATH
    )

if __name__ == "__main__":
    main()