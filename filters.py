from config import TELEGRAM_FILE_MAP

# EXACT OLD LOGIC (PORT FROM AUTO.JS)
PLAYER_MAP = {
    "messi": ["messi", "leo", "lionel"],
    "ronaldo": ["ronaldo", "cr7", "cristiano"],
    "neymar": ["neymar"],
    "mbappe": ["mbappe", "kylian"],
    "benzema": ["benzema"],
    "modric": ["modric"],
    "salah": ["salah"],
}

# ---------- BASIC ----------
def clubs():
    return sorted(TELEGRAM_FILE_MAP.keys())

def players():
    return sorted(PLAYER_MAP.keys())

def by_club(club):
    return TELEGRAM_FILE_MAP.get(club, [])

def by_player(player):
    keywords = PLAYER_MAP.get(player, [])
    out = []

    for imgs in TELEGRAM_FILE_MAP.values():
        for i in imgs:
            name = i["name"].lower()
            if any(k in name for k in keywords):
                out.append(i)

    return out

# ---------- CATEGORY ----------
def categories():
    return ["short sleeve", "full sleeve", "polo"]

def by_category(cat):
    out = []
    for imgs in TELEGRAM_FILE_MAP.values():
        for i in imgs:
            if cat in i["name"].lower():
                out.append(i)
    return out

# ---------- MIX ----------
def by_player_club(player, club):
    keywords = PLAYER_MAP.get(player, [])
    out = []

    for i in TELEGRAM_FILE_MAP.get(club, []):
        name = i["name"].lower()
        if any(k in name for k in keywords):
            out.append(i)

    return out

# ---------- TECHNIQUE ----------
def techniques():
    return ["sublimation", "embroidery", "signature"]

def by_technique(tech):
    out = []

    for imgs in TELEGRAM_FILE_MAP.values():
        for i in imgs:
            name = i["name"].lower()

            if tech == "signature" and ("signature" in name or "signed" in name):
                out.append(i)
            elif tech in name:
                out.append(i)

    return out