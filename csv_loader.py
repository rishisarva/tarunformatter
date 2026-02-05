import csv
import requests

CSV_URL = "https://visionsjersey.com/wp-content/uploads/telegram_stock.csv"

_csv_cache = None

def load_csv():
    global _csv_cache
    if _csv_cache is not None:
        return _csv_cache

    res = requests.get(CSV_URL, timeout=15)
    res.raise_for_status()

    rows = []
    reader = csv.DictReader(res.text.splitlines())
    for r in reader:
        rows.append({
            "title": r.get("title", "").strip(),
            "link": r.get("link", "").strip(),   # ✅ correct
            "image": r.get("image", "").strip() # 🔧 remove .lower()
        })

    _csv_cache = rows
    return rows


def find_from_csv(filename: str):
    filename = filename.lower()

    for row in load_csv():
        if row["image"] and row["image"] in filename:
            return row

    return None