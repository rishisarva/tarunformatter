import random
from telegram import InputMediaPhoto
from config import MAX_IMAGES

async def send_images(bot, chat_id, images):
    if not images:
        await bot.send_message(chat_id, "❌ No jerseys found")
        return

    selected = random.sample(images, min(MAX_IMAGES, len(images)))

    media = [
        InputMediaPhoto(photo=i["file_id"])
        for i in selected
    ]

    await bot.send_media_group(chat_id=chat_id, media=media)