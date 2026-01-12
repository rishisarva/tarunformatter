# cache.py

import json, os
from config import FILE_ID_CACHE

def load_cache():
    if not os.path.exists(FILE_ID_CACHE):
        return {}
    return json.load(open(FILE_ID_CACHE))

def save_cache(data):
    json.dump(data, open(FILE_ID_CACHE,"w"))