from telegram.ext import *
from telegram import Update
from config import BOT_TOKEN
from keyboards import *
from filters import *
from image_sender import send_images
from state import *

async def start(update: Update, context):
    clear(update.effective_user.id)
    await update.message.reply_text("👕 Vision Jerseys", reply_markup=main_menu())

async def buttons(update: Update, context):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id
    data = q.data

    if data == "clubs":
        await q.message.reply_text("Select Club", reply_markup=list_menu(clubs(), "club"))

    elif data.startswith("club:"):
        clear(uid)
        await send_images(context.bot, q.message.chat_id, by_club(data.split(":")[1]))

    elif data == "players":
        await q.message.reply_text("Select Player", reply_markup=list_menu(players(), "player"))

    elif data.startswith("player:"):
        clear(uid)
        await send_images(context.bot, q.message.chat_id, by_player(data.split(":")[1]))

    elif data == "categories":
        await q.message.reply_text("Select Sleeve Type", reply_markup=category_menu())

    elif data.startswith("cat:"):
        await send_images(context.bot, q.message.chat_id, by_category(data.split(":")[1]))

    elif data == "randtech":
        await q.message.reply_text("Select Technique", reply_markup=tech_menu())

    elif data.startswith("tech:"):
        await send_images(context.bot, q.message.chat_id, by_technique(data.split(":")[1]))

    elif data == "random":
        await send_images(context.bot, q.message.chat_id, all_rows(), 15)

    elif data == "wa9":
        rows = all_rows()[:9]
        for r in rows:
            caption = f"""👕 {r.get('title','Jersey')}

📏 Sizes Available:
S • M • L • XL • XXL

🔗 Product Link:
{r.get('product_link','https://visionsjersey.com')}

✨ Order now – limited stock!
"""
            await context.bot.send_photo(
                chat_id=q.message.chat_id,
                photo=r["file_id"],
                caption=caption
            )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()