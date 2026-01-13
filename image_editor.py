from PIL import Image, ImageDraw, ImageFont
import os, uuid

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
OUT_DIR = "/tmp/jersey_out"
os.makedirs(OUT_DIR, exist_ok=True)

def draw_info(image_path, number, title, price, technique):
    img = Image.open(image_path).convert("RGBA")
    W, H = img.size

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # ===== BOX SETTINGS (AutoJS-like) =====
    BOX_W = 520
    BOX_H = 160
    BOTTOM_MARGIN = 30
    RADIUS = 22

    x1 = (W - BOX_W) // 2
    y1 = H - BOX_H - BOTTOM_MARGIN
    x2 = x1 + BOX_W
    y2 = y1 + BOX_H

    draw.rounded_rectangle(
        [(x1, y1), (x2, y2)],
        radius=RADIUS,
        fill=(0, 0, 0, 170)  # low opacity black
    )

    font_big = ImageFont.truetype(FONT, 40)
    font_mid = ImageFont.truetype(FONT, 34)
    font_small = ImageFont.truetype(FONT, 30)

    def center(text, y, font):
        tw, _ = draw.textsize(text, font=font)
        draw.text(((W - tw) / 2, y), text, fill="white", font=font)

    y = y1 + 16
    center(f"No. {number}", y, font_big)
    y += 42
    center(f"{title}", y, font_mid)
    y += 36
    center(f"₹{price}  |  {technique or 'Standard'}", y, font_small)

    final = Image.alpha_composite(img, overlay)

    out = os.path.join(OUT_DIR, f"{uuid.uuid4()}.jpg")
    final.convert("RGB").save(out, "JPEG", quality=92)

    return out