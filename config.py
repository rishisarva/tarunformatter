# config.py
import requests

# ======================
# BOT CONFIG
# ======================
BOT_TOKEN = "YOUR_BOT_TOKEN"

# ======================
# TELEGRAM FILE IDS
# ======================
FILE_ID_MAP_URL = "https://raw.githubusercontent.com/rishisarva/tarunformatter/main/telegram_file_ids.json"

try:
    resp = requests.get(FILE_ID_MAP_URL, timeout=15)
    resp.raise_for_status()
    TELEGRAM_FILE_MAP = resp.json()
except Exception as e:
    raise RuntimeError(f"Failed to load telegram_file_ids.json: {e}")

# ======================
# LIMITS
# ======================
MAX_IMAGES_PER_REQUEST = 10

# ======================
# CHANNEL (INFO ONLY)
# ======================
SOURCE_CHANNEL_ID = -1003506739312