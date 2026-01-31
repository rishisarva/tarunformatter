import os
from telegram import Update
import threading
import asyncio
from http.server import BaseHTTPRequestHandler
from socketserver import TCPServer
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
from state import get, push_recent
from keyboards import recent_first_keyboard
# ================= TELEGRAM KEEP ALIVE (NO CRON, FREE) =================

KEEP_ALIVE_CHAT_ID = int(os.environ.get("KEEP_ALIVE_CHAT_ID", "0"))

async def telegram_keep_alive(app: Application):
    # wait until bot + webhook fully start
    await asyncio.sleep(30)

    while True:
        try:
            if KEEP_ALIVE_CHAT_ID != 0:
                await app.bot.send_message(
                    chat_id=KEEP_ALIVE_CHAT_ID,
                    text="."
                )
        except Exception as e:
            print("Keep-alive error:", e)

        await asyncio.sleep(300)  # 5 minutes

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

    # BACK
    if text == "⬅ back":
        context.user_data.clear()
        await update.message.reply_text("👕 Vision Jerseys", reply_markup=main_menu())
        return

    # MAIN MENU — CLUBS
    if text == "🖼 clubs":
        recent = get(update.effective_user.id, "recent_clubs") or []
        await update.message.reply_text(
            "Select Club",
            reply_markup=recent_first_keyboard(recent, clubs())
        )
        context.user_data["mode"] = "club"
        return

    # MAIN MENU — PLAYERS
    if text == "🖼 players":
        recent = get(update.effective_user.id, "recent_players") or []
        await update.message.reply_text(
            "Select Player",
            reply_markup=recent_first_keyboard(recent, players())
        )
        context.user_data["mode"] = "player"
        return

    if text == "🖼 mix":
        context.user_data["mode"] = "mix_player"
        await update.message.reply_text(
            "Select Player",
            reply_markup=list_keyboard(players())
        )
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

    # WHATSAPP RANDOM 9 (UNCHANGED)
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
        push_recent(update.effective_user.id, "recent_clubs", text)
        await send_images(context.bot, update.message.chat_id, by_club(text))
        return

    if mode == "player":
        push_recent(update.effective_user.id, "recent_players", text)
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
        await update.message.reply_text(
            "Select Club",
            reply_markup=list_keyboard(clubs())
        )
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
# ================= HEALTH SERVER (FOR UPTIMEROBOT) =================

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_health_server():
    with TCPServer(("", 8080), HealthHandler) as httpd:
        httpd.serve_forever()

def main():
    # 🔥 Start health server in background
    threading.Thread(target=run_health_server, daemon=True).start()

    app = Application.builder().token(BOT_TOKEN).build()

    # ✅ START TELEGRAM HEARTBEAT (FREE, NO CRON)
    app.post_init = lambda app: app.create_task(telegram_keep_alive(app))

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path="webhook",
        webhook_url=WEBHOOK_URL
    )
if __name__ == "__main__":
    main()
