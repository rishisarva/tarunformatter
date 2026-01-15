import random
import asyncio

IMAGE_DELAY = 0.6
MAX_IMAGES = 9

def build_caption(item):
    title = item.get("title") or item.get("name", "Premium Jersey")
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