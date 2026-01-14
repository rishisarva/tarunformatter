# image_sender.py
import random
from telegram import InputMediaPhoto

MAX_IMAGES = 10


async def send_images(bot, chat_id, images):
    if not images:
        await bot.send_message(chat_id, "❌ No jerseys found")
        return

    # pick random images (max 10)
    selected = random.sample(images, min(MAX_IMAGES, len(images)))

    media_group = [
        InputMediaPhoto(media=img["file_id"])
        for img in selected
    ]

    # 🔥 SEND AS ONE GROUP
    await bot.send_media_group(
        chat_id=chat_id,
        media=media_group
    )