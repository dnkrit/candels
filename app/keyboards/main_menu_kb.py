from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🕯 Свечи"), KeyboardButton(text="💞 Ритуал")],
            [KeyboardButton(text="🧠 НейрОракул"), KeyboardButton(text="👤 Кабинет")],
            [KeyboardButton(text="🏺 Лавка"), KeyboardButton(text="ℹ️ Помощь")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
