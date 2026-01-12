# image_sender.py

from telegram import InputMediaPhoto
from config import MODE, IMAGES_PER_ALBUM
from cache import load_cache, save_cache

cache = load_cache()

async def send_images(bot, chat_id, rows, label):
    images = [r["image"] for r in rows if r.get("image")]

    await bot.send_message(chat_id, f"━━━━ {label.upper()} STARTS HERE ━━━━")

    album = []
    for img in images:
        if MODE == "PROD" and img in cache:
            album.append(InputMediaPhoto(cache[img]))
        else:
            album.append(InputMediaPhoto(img))

        if len(album) == IMAGES_PER_ALBUM:
            msgs = await bot.send_media_group(chat_id, album)
            if MODE == "TEST":
                for m,a in zip(msgs,album):
                    cache[a.media] = m.photo[-1].file_id
                save_cache(cache)
            album=[]

    if album:
        msgs = await bot.send_media_group(chat_id, album)
        if MODE == "TEST":
            for m,a in zip(msgs,album):
                cache[a.media] = m.photo[-1].file_id
            save_cache(cache)

    await bot.send_message(chat_id, f"━━━━ {label.upper()} ENDS HERE ━━━━")