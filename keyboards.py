import random
from telegram import InputMediaPhoto

WHATSAPP_COUNT = 9

def build_whatsapp_caption(item):
    title = item.get("title", "Jersey")
    link = item.get("link", "https://visionsjersey.com")

    return (
        f"👕 {title}\n\n"
        "📏 Sizes Available:\n"
        "S • M • L • XL • XXL\n\n"
        f"🔗 Product Link:\n{link}\n\n"
        "✨ Premium quality | Limited stock\n"
        "👉 Order now before it sells out!"
    )

async def send_whatsapp_random(bot, chat_id, items):
    selected = random.sample(items, min(WHATSAPP_COUNT, len(items)))

    media = []
    for i, item in enumerate(selected):
        media.append(
            InputMediaPhoto(
                media=item["file_id"],
                caption=build_whatsapp_caption(item) if i == 0 else None
            )
        )

    await bot.send_media_group(chat_id=chat_id, media=media)