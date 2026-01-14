# image_sender.py

import random
from telegram import InputMediaPhoto
from config import MAX_IMAGES_PER_REQUEST


async def send_images(bot, chat_id, images):
    if not images:
        await bot.send_message(chat_id, "❌ No jerseys found")
        return

    selected = random.sample(
        images,
        min(MAX_IMAGES_PER_REQUEST, len(images))
    )

    media = [
        InputMediaPhoto(media=img["file_id"])
        for img in selected
    ]

    # Telegram allows max 10 per album
    await bot.send_media_group(
        chat_id=chat_id,
        media=media
    )