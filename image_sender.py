import random
from telegram import InputMediaPhoto

async def send_images(bot, chat_id, rows, limit=10):
    if not rows:
        await bot.send_message(chat_id, "❌ No jerseys found")
        return

    selected = random.sample(rows, min(limit, len(rows)))

    media = [
        InputMediaPhoto(media=r["file_id"])
        for r in selected
    ]

    await bot.send_media_group(chat_id=chat_id, media=media)