from PIL import Image, ImageDraw, ImageFont
import io, requests


def draw_info(image_url, title, price, technique):
    res = requests.get(image_url, timeout=20)
    img = Image.open(io.BytesIO(res.content)).convert("RGB")

    w, h = img.size
    draw = ImageDraw.Draw(img)

    BOX_W, BOX_H = 520, 160
    x1 = (w - BOX_W) // 2
    y1 = h - BOX_H - 30
    x2 = x1 + BOX_W
    y2 = y1 + BOX_H

    draw.rounded_rectangle(
        (x1, y1, x2, y2),
        radius=22,
        fill=(0, 0, 0, 170)
    )

    try:
        title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 38)
        text_font = ImageFont.truetype("DejaVuSans.ttf", 32)
    except:
        title_font = text_font = ImageFont.load_default()

    lines = [
        title,
        f"₹{price}",
        f"Technique: {technique}"
    ]

    y = y1 + 22
    for i, txt in enumerate(lines):
        font = title_font if i == 0 else text_font
        tw = draw.textlength(txt, font=font)
        draw.text(((w - tw) // 2, y), txt, fill="white", font=font)
        y += 44

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    buf.seek(0)
    return buf