# image_sender.py

import requests, os
from telegram import InputMediaPhoto
from image_editor import draw_info

TEMP_DIR = "/tmp/raw_images"
os.makedirs(TEMP_DIR, exist_ok=True)

async def send_images(bot, chat_id, rows, label):
    if not rows:
        await bot.send_message(chat_id, "❌ No items found")
        return

    await bot.send_message(chat_id, f"━━━━ {label.upper()} STARTS HERE ━━━━")

    index = 1

    for r in rows:
        url = r.get("image")
        if not url:
            continue

        try:
            # 1️⃣ Download image
            raw_path = os.path.join(TEMP_DIR, f"raw_{index}.jpg")
            res = requests.get(url, timeout=20)
            res.raise_for_status()

            with open(raw_path, "wb") as f:
                f.write(res.content)

            # 2️⃣ Draw overlay
            edited = draw_info(
                raw_path,
                index,
                r.get("price", "NA"),
                (r.get("techniques") or "").split("|")[0]
            )

            # 3️⃣ Send
            await bot.send_photo(
                chat_id,
                photo=open(edited, "rb"),
                caption=f"{index}. {r.get('title','Jersey')} – ₹{r.get('price','NA')}"
            )

            # 4️⃣ Cleanup
            os.remove(raw_path)
            os.remove(edited)

            index += 1

        except Exception as e:
            print("IMAGE FAIL:", e)

    await bot.send_message(chat_id, f"━━━━ {label.upper()} ENDS HERE ━━━━")