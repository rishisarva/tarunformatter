# filters.py

from config import TELEGRAM_FILE_MAP

# SAME playerMap YOU USED BEFORE
playerMap = {
    "messi": ["messi", "leo", "lionel"],
    "ronaldo": ["ronaldo", "cr7", "cristiano"],
    "neymar": ["neymar"],
    "mbappe": ["mbappe", "kylian"],
    "modric": ["modric"],
    # (keep rest unchanged)
}

def clubs():
    return sorted(TELEGRAM_FILE_MAP.keys())

def players():
    found = set()
    for club, images in TELEGRAM_FILE_MAP.items():
        for img in images:
            name = img["name"].lower()
            for p, keys in playerMap.items():
                if any(k in name for k in keys):
                    found.add(p)
    return sorted(found)

def by_club(club):
    return TELEGRAM_FILE_MAP.get(club, [])

def by_player(player):
    keys = playerMap.get(player, [])
    out = []
    for images in TELEGRAM_FILE_MAP.values():
        for img in images:
            if any(k in img["name"].lower() for k in keys):
                out.append(img)
    return out

def smart(club=None, player=None):
    out = []
    if club:
        out = by_club(club)
    if player:
        out = by_player(player)
    return out