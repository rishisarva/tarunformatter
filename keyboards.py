from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🖼 Clubs", callback_data="clubs")],
        [InlineKeyboardButton("🖼 Players", callback_data="players")],
        [InlineKeyboardButton("🧠 Smart Club / Player", callback_data="smart")],
        [InlineKeyboardButton("🖼 Categories", callback_data="categories")],
        [InlineKeyboardButton("🎯 Random Technique", callback_data="randtech")],
        [InlineKeyboardButton("🎲 Random 15 Jerseys", callback_data="random")],
        [InlineKeyboardButton("📤 WhatsApp 9 Jerseys", callback_data="wa9")]
    ])

def list_menu(items, prefix):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(i.title(), callback_data=f"{prefix}:{i}")]
        for i in items
    ])

def category_menu():
    cats = ["short sleeve", "full sleeve", "polo", "five sleeve"]
    return list_menu(cats, "cat")

def tech_menu():
    return list_menu(["sublimation","embroidery","signature"], "tech")