from config import TELEGRAM_FILE_MAP

def clubs():
    return list(TELEGRAM_FILE_MAP.keys())

def by_club(name):
    return TELEGRAM_FILE_MAP.get(name, [])

def categories():
    return ["short sleeve", "full sleeve", "polo", "five sleeve"]

def by_category(cat):
    out = []
    for imgs in TELEGRAM_FILE_MAP.values():
        for img in imgs:
            if cat.replace(" ", "_") in img["name"]:
                out.append(img)
    return out

def smart_search(query):
    q = query.lower().replace(" ", "_")
    out = []
    for imgs in TELEGRAM_FILE_MAP.values():
        for img in imgs:
            if q in img["name"]:
                out.append(img)
    return out