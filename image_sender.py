import random
import asyncio
from telegram import InputMediaPhoto

IMAGE_DELAY = 0.6
MAX_IMAGES = 9

# ---------------------------
# EXISTING HELPERS (unchanged)
# ---------------------------

def humanize_filename(name: str):
    name = name.replace(".jpg", "").replace(".png", "")
    name = name.replace("__", " ")
    name = name.replace("_", " ")
    return name.strip()

def build_caption_from_csv(row):
    title = row.get("title") or "Premium Jersey"
    link = row.get("link") or "https://visionsjersey.com"

    return (
        f"👕 {title}\n\n"
        "📏 Sizes Available:\n"
        "S • M • L • XL • XXL\n\n"
        f"🔗 Product Link:\n{link}\n\n"
        "✨ Grab yours before stock runs out!"
    )

# ------------------------------------------------
# ✅ UPDATED: send_images (NO captions, ALBUM MODE)
# ------------------------------------------------

async def send_images(bot, chat_id, images):
    if not images:
        await bot.send_message(chat_id, "❌ No jerseys found")
        return

    selected = random.sample(images, min(MAX_IMAGES, len(images)))

    media_group = [
        InputMediaPhoto(media=img["file_id"])
        for img in selected
    ]

    # Send all images together (album)
    await bot.send_media_group(
        chat_id=chat_id,
        media=media_group
    )

# ------------------------------------------------
# ✅ WHATSAPP RANDOM 9 (UNCHANGED)
# ------------------------------------------------

async def send_whatsapp_random(bot, chat_id, rows):
    if not rows:
        await bot.send_message(chat_id, "❌ CSV is empty")
        return

    selected = random.sample(rows, min(9, len(rows)))

    for row in selected:
        image_url = row.get("image")
        if not image_url:
            continue

        caption = build_caption_from_csv(row)

        await bot.send_photo(
            chat_id=chat_id,
            photo=image_url,   # URL from CSV
            caption=caption
        )
        await asyncio.sleep(IMAGE_DELAY)