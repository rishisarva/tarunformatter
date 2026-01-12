# csv_loader.py

import csv, time, requests
from config import CSV_URL, CSV_REFRESH_SECONDS

_last = 0
_rows = []

def load_csv():
    global _last, _rows

    if time.time() - _last < CSV_REFRESH_SECONDS:
        return _rows

    r = requests.get(CSV_URL, timeout=30)
    r.raise_for_status()

    reader = csv.DictReader(r.text.splitlines())
    rows = []

    for row in reader:
        row = {k: (v or "").lower() for k, v in row.items()}
        rows.append(row)

    _rows = rows
    _last = time.time()
    return rows