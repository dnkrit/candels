"""
Candels Bot — основной запуск бота Агневидцы.
FSM + Главное меню.
Обновлено: улучшено подключение FSM и маршрутов.
"""

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import CommandStart
from aiogram.types import Message

from config import settings
from app.handlers import registration, main_menu


# === Инициализация ===

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Подключение маршрутов FSM и меню
dp.include_router(registration.router)
dp.include_router(main_menu.router)


# === Стартовое сообщение ===
@dp.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(
        "✨ Добро пожаловать в храм Candels!\n"
        "Чтобы начать путешествие, введи /start или выбери пункт меню."
    )


# === Основная точка входа ===
async def main():
    print("🚀 Candels bot is running...")
    try:
        await dp.start_polling(bot, close_bot_session=True)
    except Exception as e:
        print(f"❌ Ошибка запуска Candels Bot: {e}")
    finally:
        print("🕯 Candels Bot остановлен.")


if __name__ == "__main__":
    asyncio.run(main())
