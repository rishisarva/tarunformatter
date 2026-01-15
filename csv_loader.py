import csv
import requests

CSV_URL = "https://visionsjersey.com/wp-content/uploads/telegram_stock.csv"

def load_csv():
    res = requests.get(CSV_URL, timeout=20)
    res.raise_for_status()

    reader = csv.DictReader(res.text.splitlines())
    rows = []

    for r in reader:
        if r.get("image") and r.get("title") and r.get("product_url"):
            rows.append({
                "title": r["title"].strip(),
                "image": r["image"].strip(),
                "product_url": r["product_url"].strip()
            })

    return rows