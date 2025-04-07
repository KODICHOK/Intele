from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

type_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Квартира")],
        [KeyboardButton(text="Приватний будинок")],
        [KeyboardButton(text="Офіс")],
        [KeyboardButton(text="Склад")],
    ],
    resize_keyboard=True
)

area_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="До 50 м²")],
        [KeyboardButton(text="50–100 м²")],
        [KeyboardButton(text="Понад 100 м²")],
    ],
    resize_keyboard=True
)

yes_no_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Так")],
        [KeyboardButton(text="Ні")],
    ],
    resize_keyboard=True
)
