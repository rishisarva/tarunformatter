import requests

BOT_TOKEN = "YOUR_BOT_TOKEN"

FILE_ID_MAP_URL = "https://raw.githubusercontent.com/rishisarva/tarunformatter/main/telegram_file_ids.json"

try:
    TELEGRAM_FILE_MAP = requests.get(FILE_ID_MAP_URL, timeout=15).json()
except Exception as e:
    raise RuntimeError(f"Failed to load telegram_file_ids.json: {e}")

MAX_IMAGES_PER_REQUEST = 10
SOURCE_CHANNEL_ID = -1003506739312