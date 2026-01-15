from config import TELEGRAM_FILE_MAP

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