from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

FONT_SIZE_TITLE = 36
FONT_SIZE_META = 30
BOX_HEIGHT = 160
BOX_OPACITY = 170  # 0–255

def render_image(url, title, price, technique):
    r = requests.get(url, timeout=30)
    r.raise_for_status()

    img = Image.open(BytesIO(r.content)).convert("RGBA")
    w, h = img.size

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    box_w = int(w * 0.75)
    x1 = (w - box_w) // 2
    y1 = h - BOX_HEIGHT - 25
    x2 = x1 + box_w
    y2 = y1 + BOX_HEIGHT

    draw.rounded_rectangle(
        [x1, y1, x2, y2],
        radius=25,
        fill=(0, 0, 0, BOX_OPACITY)
    )

    try:
        font_bold = ImageFont.truetype("DejaVuSans-Bold.ttf", FONT_SIZE_TITLE)
        font = ImageFont.truetype("DejaVuSans.ttf", FONT_SIZE_META)
    except:
        font_bold = font = ImageFont.load_default()

    cx = w // 2
    ty = y1 + 20

    draw.text((cx, ty), title, font=font_bold, fill="white", anchor="mm")
    draw.text((cx, ty + 45), f"Price - ₹{price}", font=font, fill="white", anchor="mm")
    draw.text(
        (cx, ty + 85),
        f"Technique - {technique or 'Standard'}",
        font=font,
        fill="white",
        anchor="mm"
    )

    final = Image.alpha_composite(img, overlay).convert("RGB")
    return final