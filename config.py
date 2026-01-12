# config.py

import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

# ================= MODE =================
# TEST  -> uploads images once
# PROD  -> uses cached file_id (FAST AS HELL)
MODE = "TEST"   # CHANGE TO "PROD" AFTER FIRST SUCCESS

# ================= CSV =================
CSV_URL = "https://visionsjersey.com/wp-content/uploads/telegram_stock.csv"
CSV_REFRESH_SECONDS = 15 * 60

# ================= IMAGES =================
IMAGES_PER_ALBUM = 10

# ================= CACHE =================
FILE_ID_CACHE = "file_id_cache.json"