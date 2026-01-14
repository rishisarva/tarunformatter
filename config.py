import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN") or "PUT_YOUR_TOKEN"

FILE_ID_MAP_URL = "https://raw.githubusercontent.com/rishisarva/tarunformatter/main/telegram_file_ids.json"

resp = requests.get(FILE_ID_MAP_URL, timeout=20)
resp.raise_for_status()
TELEGRAM_FILE_MAP = resp.json()

MAX_IMAGES = 10