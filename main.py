"""
Candels Bot — главный модуль Telegram-бота.
Запускает FSM, регистрирует хендлеры и подключает CRUD.
"""

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from config import settings
from app.database import crud, session

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


@dp.message(lambda m: m.text.lower() in ["start", "/start"])
async def start_cmd(message: Message):
    """Приветственное сообщение"""
    await message.answer("✨ Добро пожаловать в Candels — выбери свой ритуал или создай свечу!")


@dp.message(lambda m: m.text.lower() == "мой профиль")
async def show_profile(message: Message):
    """Пример запроса к БД"""
    db = session.SessionLocal()
    user = crud.get_user_profile(db, user_id="test-user-id")  # пример вызова
    if user:
        await message.answer(f"👤 {user.name}, ваш знак — {user.zodiac_west}")
    else:
        await message.answer("Профиль не найден.")
    db.close()


async def main():
    print("🚀 Candels bot is running...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
