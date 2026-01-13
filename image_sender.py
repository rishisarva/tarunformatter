import random
from telegram import InputMediaPhoto
from image_editor import draw_info


async def send_images(bot, chat_id, rows, label):
    rows = [r for r in rows if r.get("image")]
    if not rows:
        await bot.send_message(chat_id, "❌ No images found")
        return

    selected = random.sample(rows, min(10, len(rows)))
    album = []

    for r in selected:
        img = draw_info(
            r["image"],
            r.get("title", "Jersey"),
            r.get("price", "NA"),
            (r.get("techniques") or "Standard").split("|")[0]
        )
        album.append(InputMediaPhoto(img))

    await bot.send_media_group(chat_id, album)