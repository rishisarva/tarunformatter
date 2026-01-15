from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🏟 Clubs", callback_data="clubs")],
        [InlineKeyboardButton("👤 Players", callback_data="players")],
        [InlineKeyboardButton("🧠 Smart Club / Player", callback_data="smart")],
        [InlineKeyboardButton("🧩 Categories", callback_data="categories")],
        [InlineKeyboardButton("🎲 Random 9 (WhatsApp)", callback_data="random_9")]
    ])

def sleeve_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👕 Short Sleeve", callback_data="cat_short")],
        [InlineKeyboardButton("👔 Full Sleeve", callback_data="cat_full")],
        [InlineKeyboardButton("🧥 Polo", callback_data="cat_polo")],
        [InlineKeyboardButton("👚 Five Sleeve", callback_data="cat_five")]
    ])