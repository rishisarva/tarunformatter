import random
import asyncio
import requests

IMAGE_DELAY = 0.8
MAX_IMAGES = 9

def build_caption(row):
    return (
        f"👕 {row['title']}\n\n"
        "📏 Sizes Available:\n"
        "S • M • L • XL • XXL\n\n"
        f"🔗 Product Link:\n{row['product_url']}\n\n"
        "✨ Grab yours before stock runs out!"
    )

async def send_whatsapp_random(bot, chat_id, csv_rows):
    if not csv_rows:
        await bot.send_message(chat_id, "❌ No products found")
        return

    selected = random.sample(csv_rows, min(MAX_IMAGES, len(csv_rows)))

    for row in selected:
        await bot.send_photo(
            chat_id=chat_id,
            photo=row["image"],   # 🔥 DIRECT IMAGE URL
            caption=build_caption(row)
        )
        await asyncio.sleep(IMAGE_DELAY)