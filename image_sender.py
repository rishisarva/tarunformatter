# image_sender.py

import random
from config import TELEGRAM_FILE_MAP, MAX_IMAGES_PER_REQUEST


def send_images(bot, chat_id, images):
    """
    images = list of {name, file_id}
    """
    if not images:
        await_or_send(bot, chat_id, "❌ No jerseys found")
        return

    selected = random.sample(
        images,
        min(MAX_IMAGES_PER_REQUEST, len(images))
    )

    for img in selected:
        bot.send_photo(
            chat_id=chat_id,
            photo=img["file_id"]
        )


def await_or_send(bot, chat_id, text):
    """
    Safe sync send helper (python-telegram-bot v21+)
    """
    try:
        bot.send_message(chat_id=chat_id, text=text)
    except Exception:
        pass