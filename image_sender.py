# image_sender.py

import json, random
from config import FILE_ID_MAP_PATH, IMAGE_COUNT

# load once at startup
with open(FILE_ID_MAP_PATH, "r") as f:
    FILE_MAP = json.load(f)


def get_images_by_club(club_slug):
    return FILE_MAP.get(club_slug, [])


def send_images(bot, chat_id, images):
    """
    images = list of {name, file_id}
    """
    if not images:
        bot.send_message(chat_id, "❌ No jerseys found")
        return

    selected = random.sample(images, min(IMAGE_COUNT, len(images)))

    for img in selected:
        bot.send_photo(chat_id, photo=img["file_id"])