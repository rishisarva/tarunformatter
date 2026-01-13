from telegram import InputMediaPhoto
from image_editor import render_image
from io import BytesIO

async def send_images(bot, chat_id, rows, label):
    if not rows:
        await bot.send_message(chat_id, "❌ No images found.")
        return

    await bot.send_message(chat_id, f"━━━━ {label.upper()} STARTS HERE ━━━━")

    album = []

    for r in rows[:15]:
        try:
            img = render_image(
                r["image"],
                r.get("title", "Jersey"),
                r.get("price", "NA"),
                r.get("techniques", "")
            )

            bio = BytesIO()
            img.save(bio, format="JPEG", quality=95)
            bio.seek(0)

            album.append(InputMediaPhoto(bio))

            if len(album) == 10:
                await bot.send_media_group(chat_id, album)
                album = []

        except Exception as e:
            print("IMAGE ERROR:", e)

    if album:
        await bot.send_media_group(chat_id, album)

    await bot.send_message(chat_id, f"━━━━ {label.upper()} ENDS HERE ━━━━")