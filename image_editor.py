# image_editor.py

from PIL import Image, ImageDraw, ImageFont
import os
import uuid

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
OUTPUT_DIR = "/tmp/jersey_images"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def draw_info(image_path, number, price, technique):
    img = Image.open(image_path).convert("RGBA")
    w, h = img.size

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # ===== Box size (fixed like AutoJS) =====
    BOX_W = 500
    BOX_H = 150
    BOTTOM_MARGIN = 30
    RADIUS = 20

    x1 = (w - BOX_W) // 2
    y1 = h - BOX_H - BOTTOM_MARGIN
    x2 = x1 + BOX_W
    y2 = y1 + BOX_H

    draw.rounded_rectangle(
        [(x1, y1), (x2, y2)],
        radius=RADIUS,
        fill=(0, 0, 0, 170)
    )

    font_big = ImageFont.truetype(FONT_PATH, 42)
    font_small = ImageFont.truetype(FONT_PATH, 34)

    def center_text(text, y, font):
        tw, th = draw.textsize(text, font=font)
        draw.text(((w - tw) / 2, y), text, fill="white", font=font)

    y = y1 + 18
    center_text(f"No. {number}", y, font_big)
    y += 44
    center_text(f"Price - ₹{price}", y, font_small)
    y += 38
    center_text(f"Technique - {technique or 'Standard'}", y, font_small)

    final = Image.alpha_composite(img, overlay)

    out_path = os.path.join(OUTPUT_DIR, f"{uuid.uuid4()}.jpg")
    final.convert("RGB").save(out_path, "JPEG", quality=92)

    return out_path