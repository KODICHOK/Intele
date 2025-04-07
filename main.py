from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from keyboards import type_keyboard, area_keyboard, yes_no_keyboard

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


class Survey(StatesGroup):
    type = State()
    area = State()
    night = State()
    cloud = State()
    cameras = State()
    budget = State()


@dp.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await message.answer("Привіт! Я допоможу підібрати систему відеоспостереження.\nОбери тип об'єкта:",
                         reply_markup=type_keyboard)
    await state.set_state(Survey.type)


@dp.message(Survey.type)
async def get_type(message: Message, state: FSMContext):
    await state.update_data(type=message.text)
    await message.answer("Яка приблизна площа об'єкта?", reply_markup=area_keyboard)
    await state.set_state(Survey.area)


@dp.message(Survey.area)
async def get_area(message: Message, state: FSMContext):
    await state.update_data(area=message.text)
    await message.answer("Чи потрібне нічне бачення?", reply_markup=yes_no_keyboard)
    await state.set_state(Survey.night)


@dp.message(Survey.night)
async def get_night(message: Message, state: FSMContext):
    await state.update_data(night=message.text)
    await message.answer("Чи потрібен запис у хмару?", reply_markup=yes_no_keyboard)
    await state.set_state(Survey.cloud)


@dp.message(Survey.cloud)
async def get_cloud(message: Message, state: FSMContext):
    await state.update_data(cloud=message.text)
    await message.answer("Скільки камер вам потрібно?")
    await state.set_state(Survey.cameras)


@dp.message(Survey.cameras)
async def get_cameras(message: Message, state: FSMContext):
    await state.update_data(cameras=message.text)
    await message.answer("Який у вас бюджет? (в грн)")
    await state.set_state(Survey.budget)


@dp.message(Survey.budget)
async def get_budget(message: Message, state: FSMContext):
    await state.update_data(budget=message.text)
    data = await state.get_data()

    recommendation = f"""
🔎 *Рекомендація для вас:*

📍 Об'єкт: {data['type']}
📐 Площа: {data['area']}
🌙 Нічне бачення: {data['night']}
☁️ Запис у хмару: {data['cloud']}
📷 Кількість камер: {data['cameras']}
💰 Бюджет: {data['budget']} грн

✅ Вам підійде комплект з {data['cameras']} IP-камер з роздільною здатністю 1080p, з нічним баченням — {data['night']}, та з хмарним записом — {data['cloud']}. Орієнтовна ціна: {data['budget']} грн.
    """
    await message.answer(recommendation, parse_mode="Markdown")
    await state.clear()


if __name__ == "__main__":
    import asyncio

    asyncio.run(dp.start_polling(bot))
