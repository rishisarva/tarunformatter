# keyboards.py

from telegram import ReplyKeyboardMarkup

def main_menu():
    return ReplyKeyboardMarkup([
        ["🖼 Clubs", "🖼 Players"],
        ["🧠 Smart Club / Player", "🎲 Random 15 Jerseys"],
        ["🖼 Mix", "🖼 Categories"],
        ["🎯 Random Technique"],
    ], resize_keyboard=True)

def back_menu():
    return ReplyKeyboardMarkup([["⬅ Back"]], resize_keyboard=True)

def list_menu(items):
    return ReplyKeyboardMarkup([[i] for i in items] + [["⬅ Back"]], resize_keyboard=True)