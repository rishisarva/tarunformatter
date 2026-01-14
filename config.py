# config.py
import os
import requests

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not set in environment")

FILE_ID_MAP_URL = "https://raw.githubusercontent.com/rishisarva/tarunformatter/main/telegram_file_ids.json"

resp = requests.get(FILE_ID_MAP_URL, timeout=15)
resp.raise_for_status()
TELEGRAM_FILE_MAP = resp.json()

MAX_IMAGES_PER_REQUEST = 10
SOURCE_CHANNEL_ID = -1003506739312