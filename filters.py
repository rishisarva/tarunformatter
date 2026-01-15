from config import TELEGRAM_FILE_MAP

# ---------- BASIC ----------
def clubs():
    return sorted(TELEGRAM_FILE_MAP.keys())

def players():
    players = set()
    for imgs in TELEGRAM_FILE_MAP.values():
        for i in imgs:
            name = i["name"].lower()
            players.add(name.split("__")[1] if "__" in name else name)
    return sorted(players)

def by_club(club):
    return TELEGRAM_FILE_MAP.get(club, [])

def by_player(player):
    out = []
    for imgs in TELEGRAM_FILE_MAP.values():
        out += [i for i in imgs if player in i["name"].lower()]
    return out

# ---------- CATEGORY (SLEEVE) ----------
def categories():
    return ["short sleeve", "full sleeve", "polo"]

def by_category(cat):
    out = []
    for imgs in TELEGRAM_FILE_MAP.values():
        for i in imgs:
            if cat in i["name"].lower():
                out.append(i)
    return out

# ---------- MIX (PLAYER + CLUB) ----------
def by_player_club(player, club):
    out = []
    for i in TELEGRAM_FILE_MAP.get(club, []):
        if player in i["name"].lower():
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