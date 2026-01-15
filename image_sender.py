import random
import asyncio

IMAGE_DELAY = 0.6
MAX_IMAGES = 9

async def send_images(bot, chat_id, images, caption=None):
    if not images:
        await bot.send_message(chat_id, "❌ No jerseys found")
        return

    selected = random.sample(images, min(MAX_IMAGES, len(images)))

    for idx, img in enumerate(selected):
        await bot.send_photo(
            chat_id=chat_id,
            photo=img["file_id"],
            caption=caption if idx == 0 else None
        )
        await asyncio.sleep(IMAGE_DELAY)