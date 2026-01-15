import random
import asyncio
from csv_loader import find_from_csv

IMAGE_DELAY = 0.6
MAX_IMAGES = 9


def humanize_filename(name: str):
    name = name.replace(".jpg", "").replace(".png", "")
    name = name.replace("__", " ")
    name = name.replace("_", " ")
    return name.strip()


def build_caption(item):
    filename = item.get("name", "").lower()
    csv_row = find_from_csv(filename)

    if csv_row and csv_row["title"] and csv_row["link"]:
        title = csv_row["title"]
        link = csv_row["link"]
    else:
        title = humanize_filename(filename)
        link = "https://visionsjersey.com"

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