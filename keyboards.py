from telegram import ReplyKeyboardMarkup

def main_menu():
    return ReplyKeyboardMarkup(
        [
            ["🖼 Clubs", "🖼 Players"],
            ["🖼 Mix", "🖼 Categories"],
            ["🎯 Random Technique"],
            ["📲 WhatsApp Random 9"],
            ["🎲 Random Jerseys"]
        ],
        resize_keyboard=True
    )

def list_keyboard(items):
    rows = []
    for i in range(0, len(items), 2):
        row = [items[i].title()]
        if i + 1 < len(items):
            row.append(items[i+1].title())
        rows.append(row)

    rows.append(["⬅ Back"])
    return ReplyKeyboardMarkup(rows, resize_keyboard=True)


def recent_first_keyboard(recent, all_items):
    keyboard = []

    # 🔥 Recent first
    for r in recent:
        keyboard.append([r])

    # separator (non-clickable visual)
    if recent:
        keyboard.append(["────────────"])

    # 📂 All items
    for item in all_items:
        keyboard.append([item])

    keyboard.append(["⬅ Back"])

    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)