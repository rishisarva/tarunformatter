import random
from telegram import InputMediaPhoto

MAX_IMAGES = 9  # WhatsApp-friendly

async def send_images(bot, chat_id, images, caption=None):
    if not images:
        await bot.send_message(chat_id, "❌ No jerseys found")
        return

    selected = random.sample(images, min(MAX_IMAGES, len(images)))

    media = []
    for i, img in enumerate(selected):
        media.append(
            InputMediaPhoto(
                media=img["file_id"],
                caption=caption if i == 0 else None
            )
        )

    await bot.send_media_group(chat_id=chat_id, media=media)