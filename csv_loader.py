BASE_IMAGE_URL = "https://visionsjersey.com/wp-content/uploads/"

def load_csv():
    global _csv_cache
    if _csv_cache is not None:
        return _csv_cache

    res = requests.get(CSV_URL, timeout=15)
    res.raise_for_status()

    rows = []
    reader = csv.DictReader(res.text.splitlines())
    for r in reader:
        image_name = r.get("image", "").strip()

        rows.append({
            "title": r.get("title", "").strip(),
            "link": r.get("link", "").strip(),
            "image": BASE_IMAGE_URL + image_name if image_name else ""
        })

    _csv_cache = rows
    return rows