# image_sender.py
import random
import asyncio

IMAGE_DELAY = 0.6  # prevents Telegram flood block
MAX_IMAGES = 10


async def send_images(bot, chat_id, images):
    if not images:
        await bot.send_message(chat_id, "❌ No jerseys found")
        return

    selected = random.sample(images, min(MAX_IMAGES, len(images)))

    for img in selected:
        await bot.send_photo(
            chat_id=chat_id,
            photo=img["file_id"]
        )
        await asyncio.sleep(IMAGE_DELAY)