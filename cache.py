# cache.py

import time, requests, json

_file_ids = {}
_last = 0
TTL = 300  # 5 min

def get_file_ids(url):
    global _file_ids, _last

    if time.time() - _last < TTL:
        return _file_ids

    r = requests.get(url, timeout=20)
    r.raise_for_status()

    _file_ids = r.json()
    _last = time.time()
    return _file_ids