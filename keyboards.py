from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🖼 Clubs", callback_data="clubs")],
        [InlineKeyboardButton("🖼 Players", callback_data="players")],
        [InlineKeyboardButton("🖼 Categories", callback_data="categories")],
        [InlineKeyboardButton("🧠 Smart Club / Player", callback_data="smart")],
        [InlineKeyboardButton("🎲 Random Jerseys", callback_data="random")],
        [InlineKeyboardButton("📤 WhatsApp 9 Jerseys", callback_data="wa_post")]
    ])

def list_menu(items, prefix):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(i.title(), callback_data=f"{prefix}:{i}")]
        for i in items
    ])