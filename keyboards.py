from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🖼 Clubs", callback_data="menu:clubs"),
         InlineKeyboardButton("🖼 Players", callback_data="menu:players")],
        [InlineKeyboardButton("🧠 Smart Filter", callback_data="menu:smart")],
        [InlineKeyboardButton("🎲 Random Jerseys", callback_data="menu:random")],
        [InlineKeyboardButton("🖼 Categories", callback_data="menu:categories")],
        [InlineKeyboardButton("🎯 Random Technique", callback_data="menu:technique")]
    ])

def back_btn():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅ Back", callback_data="menu:back")]
    ])

def list_buttons(items, prefix):
    rows = []
    for i in range(0, len(items), 2):
        row = [
            InlineKeyboardButton(items[i].title(), callback_data=f"{prefix}:{items[i]}")
        ]
        if i + 1 < len(items):
            row.append(
                InlineKeyboardButton(items[i+1].title(), callback_data=f"{prefix}:{items[i+1]}")
            )
        rows.append(row)

    rows.append([InlineKeyboardButton("⬅ Back", callback_data="menu:back")])
    return InlineKeyboardMarkup(rows)