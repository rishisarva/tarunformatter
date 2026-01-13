# image_sender.py

from telegram import InputMediaPhoto
from config import MODE, IMAGES_PER_ALBUM
from cache import load_cache, save_cache

cache = load_cache()

async def send_images(bot, chat_id, rows, label):
    images = [r.get("image") for r in rows if r.get("image")]

    if not images:
        await bot.send_message(chat_id, "❌ No images found.")
        return

    await bot.send_message(chat_id, f"━━━━ {label.upper()} STARTS HERE ━━━━")

    album = []

    for img in images:
        try:
            if MODE == "PROD" and img in cache:
                album.append(InputMediaPhoto(cache[img]))
            else:
                album.append(InputMediaPhoto(img))
        except Exception:
            continue  # skip broken URL

        if len(album) == IMAGES_PER_ALBUM:
            try:
                msgs = await bot.send_media_group(chat_id, album)
                if MODE == "TEST":
                    for m, a in zip(msgs, album):
                        cache[a.media] = m.photo[-1].file_id
                    save_cache(cache)
            except Exception:
                pass  # skip failed batch

            album = []

    if album:
        try:
            msgs = await bot.send_media_group(chat_id, album)
            if MODE == "TEST":
                for m, a in zip(msgs, album):
                    cache[a.media] = m.photo[-1].file_id
                save_cache(cache)
        except Exception:
            pass

    await bot.send_message(chat_id, f"━━━━ {label.upper()} ENDS HERE ━━━━")