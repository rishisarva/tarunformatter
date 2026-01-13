# image_sender.py
from telegram import InputMediaPhoto

async def send_images(bot, chat_id, rows, label):
    images = [r.get("image") for r in rows if r.get("image")]

    if not images:
        await bot.send_message(chat_id, "❌ No images found.")
        return

    await bot.send_message(chat_id, f"━━━━ {label.upper()} STARTS HERE ━━━━")

    album = []
    for img in images:
        album.append(InputMediaPhoto(img))

        if len(album) == 10:  # Telegram limit
            await bot.send_media_group(chat_id, album)
            album = []

    if album:
        await bot.send_media_group(chat_id, album)

    await bot.send_message(chat_id, f"━━━━ {label.upper()} ENDS HERE ━━━━")