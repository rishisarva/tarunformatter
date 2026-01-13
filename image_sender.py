# image_sender.py

from telegram import InputMediaPhoto
from cache import get_file_ids
from config import FILE_ID_MAP_URL, MAX_IMAGES_PER_REQUEST
import random

async def send_images(bot, chat_id, club_key):
    file_map = get_file_ids(FILE_ID_MAP_URL)

    images = file_map.get(club_key.lower(), [])
    if not images:
        await bot.send_message(chat_id, "❌ No images found.")
        return

    # 🎯 pick non-repeating 10
    selected = random.sample(
        images,
        min(MAX_IMAGES_PER_REQUEST, len(images))
    )

    media = [
        InputMediaPhoto(media=img["file_id"])
        for img in selected
    ]

    await bot.send_media_group(chat_id=chat_id, media=media)