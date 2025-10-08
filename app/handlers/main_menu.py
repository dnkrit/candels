"""
Обработчики главного меню Candels Bot.
После регистрации пользователь попадает сюда.
"""

from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardRemove
from app.keyboards.main_menu_kb import get_main_menu

router = Router()


# === Обработка /menu или кнопки "🏠 Меню" ===
@router.message(Command("menu"))
async def show_main_menu(message: types.Message):
    await message.answer(
        "🏠 Главное меню Candels.\n"
        "Выбери раздел, который откроет тебе путь света 🔮",
        reply_markup=get_main_menu()
    )


# === 🕯 Свечи ===
@router.message(F.text == "🕯 Свечи")
async def candles_menu(message: types.Message):
    await message.answer(
        "🕯 Здесь ты можешь создать свою магическую свечу.\n"
        "Выбери форму, цвет и энергию, которые откликнутся твоему духу ✨",
        reply_markup=ReplyKeyboardRemove()
    )


# === 💞 Ритуал ===
@router.message(F.text == "💞 Ритуал")
async def ritual_menu(message: types.Message):
    await message.answer(
        "💞 Ритуалы Агневидцы помогут тебе в любви, успехе и исцелении.\n"
        "Выбери направление, и мы подскажем свечу и руну для гармонии 🔮"
    )


# === 🧠 НейрОракул ===
@router.message(F.text == "🧠 НейрОракул")
async def neuro_oracle(message: types.Message):
    await message.answer(
        "🧠 НейрОракул готов раскрыть подсознательные знаки.\n"
        "Сосредоточься на своём вопросе и нажми /oracle 🔮"
    )


# === 👤 Кабинет ===
@router.message(F.text == "👤 Кабинет")
async def user_profile(message: types.Message):
    await message.answer(
        f"👤 Профиль пользователя @{message.from_user.username or message.from_user.first_name}\n"
        f"✨ Здесь будут твои свечи, ритуалы и подписки."
    )


# === 🏺 Лавка ===
@router.message(F.text == "🏺 Лавка")
async def shop_section(message: types.Message):
    await message.answer(
        "🏺 В лавке Агневидцы ты найдёшь свечи силы, амулеты и дары стихий 🔥"
    )


# === ℹ️ Помощь ===
@router.message(F.text == "ℹ️ Помощь")
async def show_help(message: types.Message):
    await message.answer(
        "ℹ️ Добро пожаловать в Candels!\n\n"
        "✨ Доступные команды:\n"
        "/start — регистрация\n"
        "/menu — главное меню\n"
        "/oracle — НейрОракул\n\n"
        "Связаться с мастером 🔮: @Agnevidca_support"
    )
