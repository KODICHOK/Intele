
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

class Phone:
    def __init__(self, brand, model, price):
        self.brand = brand
        self.model = model
        self.price = price

    def __str__(self):
        return f"{self.brand} {self.model} - {self.price} грн"

phones = [
    Phone("Apple", "iPhone 14", 40000),
    Phone("Samsung", "Galaxy S23", 35000),
    Phone("Xiaomi", "Redmi Note 13", 12000),
    Phone("OnePlus", "11 Pro", 30000)
]

user_carts = {}

def get_main_menu():
    return [["📱 Телефони", "🛒 Кошик"], ["✅ Замовити", "❌ Очистити"]]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_carts[user.id] = []
    await update.message.reply_text(
        f"Привіт, {user.first_name}! 👋\nЯ допоможу тобі замовити мобільний телефон.",
        reply_markup=ReplyKeyboardMarkup(get_main_menu(), resize_keyboard=True)
    )

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if text == "📱 Телефони":
        msg = "Доступні телефони:\n"
        for i, p in enumerate(phones, start=1):
            msg += f"{i}. {p}\n"
        msg += "\nВведи номер телефону для додавання до кошика."
        await update.message.reply_text(msg)

    elif text.isdigit():
        index = int(text) - 1
        if 0 <= index < len(phones):
            user_carts.setdefault(user_id, []).append(phones[index])
            await update.message.reply_text(f"{phones[index]} додано до кошика ✅")
        else:
            await update.message.reply_text("Невірний номер телефону.")

    elif text == "🛒 Кошик":
        cart = user_carts.get(user_id, [])
        if not cart:
            await update.message.reply_text("Ваш кошик порожній.")
        else:
            msg = "Ваш кошик:\n"
            total = 0
            for p in cart:
                msg += f"- {p}\n"
                total += p.price
            msg += f"\nЗагальна сума: {total} грн"
            await update.message.reply_text(msg)

    elif text == "✅ Замовити":
        cart = user_carts.get(user_id, [])
        if not cart:
            await update.message.reply_text("Кошик порожній 😢")
        else:
            total = sum(p.price for p in cart)
            await update.message.reply_text(f"Дякуємо за замовлення на суму {total} грн! 📦\nМенеджер з вами зв'яжеться.")
            user_carts[user_id] = []

    elif text == "❌ Очистити":
        user_carts[user_id] = []
        await update.message.reply_text("Кошик очищено.")

    else:
        await update.message.reply_text("Виберіть дію з меню ⬇️")

async def main():
    TOKEN = "7532983760:AAFqY5JF_fzqRaRwtQ7QV4fvtaG-2uoy1AY"  # ← сюди встав свій Telegram Bot Token
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    print("Бот запущено!")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
