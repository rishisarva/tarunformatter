import os
import requests

BOT_TOKEN = os.environ.get("BOT_TOKEN")

FILE_ID_MAP_URL = "https://raw.githubusercontent.com/rishisarva/tarunformatter/main/telegram_file_ids.json"

resp = requests.get(FILE_ID_MAP_URL, timeout=15)
resp.raise_for_status()
TELEGRAM_FILE_MAP = resp.json()

MAX_IMAGES = 9

WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = os.environ.get("RENDER_EXTERNAL_URL") + WEBHOOK_PATH