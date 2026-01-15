import random
from telegram import InputMediaPhoto

SIZES_TEXT = "S • M • L • XL • XXL"

async def send_whatsapp_random(bot, chat_id, rows, count=9):
    if not rows:
        await bot.send_message(chat_id, "❌ No products found.")
        return

    picks = random.sample(rows, min(count, len(rows)))

    media = []

    for r in picks:
        image = r.get("image", "").strip()
        title = r.get("title", "").strip()
        link = r.get("link", "").strip()   # ✅ FIXED HERE

        if not image:
            continue

        caption = (
            f"👕 {title}\n\n"
            f"📏 Sizes Available:\n"
            f"{SIZES_TEXT}\n\n"
            f"🔗 Product Link:\n{link}\n\n"
            f"✨ Grab yours before stock runs out!"
        )

        media.append(
            InputMediaPhoto(
                media=image,
                caption=caption
            )
        )

    if not media:
        await bot.send_message(chat_id, "❌ No valid products found.")
        return

    await bot.send_media_group(chat_id, media)