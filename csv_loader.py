import csv
import requests

CSV_URL = "https://visionsjersey.com/wp-content/uploads/telegram_stock.csv"

_csv_cache = None

def load_csv():
    global _csv_cache

    # 🔥 DO NOT cache forever (latest stock)
    _csv_cache = None

    res = requests.get(CSV_URL, timeout=20)
    res.raise_for_status()

    rows = []
    reader = csv.DictReader(res.text.splitlines())

    for r in reader:
        image_name = r.get("image", "").strip()

        if not image_name:
            continue

        rows.append({
            "title": r.get("title", "").strip(),
            "link": r.get("link", "").strip(),
            "image": BASE_IMAGE_URL + image_name   # ✅ FULL URL
        })

    return rows

def find_from_csv(filename: str):
    filename = filename.lower()

    for row in load_csv():
        if row["image"] and row["image"] in filename:
            return row

    return None