import csv
import requests
import os
from urllib.parse import urlparse

CSV_URL = "https://visionsjersey.com/wp-content/uploads/telegram_stock.csv"

_csv_cache = None


def _basename(url: str) -> str:
    """Extract filename from image URL"""
    try:
        return os.path.basename(urlparse(url).path).lower()
    except Exception:
        return ""


def load_csv():
    global _csv_cache
    if _csv_cache is not None:
        return _csv_cache

    res = requests.get(CSV_URL, timeout=15)
    res.raise_for_status()

    rows = []
    reader = csv.DictReader(res.text.splitlines())

    for r in reader:
        image_url = r.get("image", "").strip()

        rows.append({
            "title": r.get("title", "").strip(),
            "link": r.get("link", "").strip(),   # ✅ CORRECT COLUMN
            "image_name": _basename(image_url)  # ✅ filename only
        })

    _csv_cache = rows
    return rows


def find_from_csv(filename: str):
    filename = filename.lower()

    for row in load_csv():
        if row["image_name"] and row["image_name"] in filename:
            return row

    return None