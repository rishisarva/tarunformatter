import random
import asyncio

IMAGE_DELAY = 0.6
MAX_IMAGES = 9

import re

def prettify_name(raw):
    # remove extension
    name = raw.rsplit(".", 1)[0]

    # replace __ and _
    name = name.replace("__", " ").replace("_", " ")

    # fix seasons like 2008 09 → 2008-09
    name = re.sub(r"(\d{4}) (\d{2})", r"\1-\2", name)

    # clean extra spaces
    name = re.sub(r"\s+", " ", name).strip()

    return name.title()


def build_caption(item):
    if "title" in item and item["title"]:
        title = item["title"]
    else:
        title = prettify_name(item.get("name", "Premium Jersey"))

    link = item.get("link", "https://visionsjersey.com")

    return (
        f"👕 {title}\n\n"
        "📏 Sizes Available:\n"
        "S • M • L • XL • XXL\n\n"
        f"🔗 Product Link:\n{link}\n\n"
        "✨ Grab yours before stock runs out!"
    )

async def send_images(bot, chat_id, images):
    if not images:
        await bot.send_message(chat_id, "❌ No jerseys found")
        return

    selected = random.sample(images, min(MAX_IMAGES, len(images)))

    for img in selected:
        await bot.send_photo(
            chat_id=chat_id,
            photo=img["file_id"],
            caption=build_caption(img)
        )
        await asyncio.sleep(IMAGE_DELAY)