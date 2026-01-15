from config import TELEGRAM_FILE_MAP
from state import *

def all_rows():
    rows = []
    for items in TELEGRAM_FILE_MAP.values():
        rows.extend(items)
    return rows

def clubs():
    return sorted(set(r["club"] for r in all_rows() if "club" in r))

def players():
    return sorted(set(r["player"] for r in all_rows() if "player" in r))

def by_club(name):
    return [r for r in all_rows() if r.get("club","").lower() == name.lower()]

def by_player(name):
    return [r for r in all_rows() if name.lower() in r.get("title","").lower()]

def by_category(category):
    return [r for r in all_rows() if category in r.get("title","").lower()]

def by_technique(tech):
    return [
        r for r in all_rows()
        if tech in r.get("title","").lower()
        or tech in r.get("techniques","").lower()
    ]