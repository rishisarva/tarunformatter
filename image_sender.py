import requests, os
from image_editor import draw_info

TMP = "/tmp/raw"
os.makedirs(TMP, exist_ok=True)

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
            raw = os.path.join(TMP, f"raw_{index}.jpg")
            res = requests.get(url, timeout=20)
            res.raise_for_status()
            open(raw, "wb").write(res.content)

            edited = draw_info(
                raw,
                index,
                r.get("title", "Jersey"),
                r.get("price", "NA"),
                (r.get("techniques") or "").split("|")[0]
            )

            await bot.send_photo(
                chat_id,
                photo=open(edited, "rb")
            )

            os.remove(raw)
            os.remove(edited)

            index += 1

        except Exception as e:
            print("IMAGE ERROR:", e)

    await bot.send_message(chat_id, f"━━━━ {label.upper()} ENDS HERE ━━━━")