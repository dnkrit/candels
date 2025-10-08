"""
FSM-хендлеры регистрации пользователя для Candels Bot (обновлено).
"""

from datetime import datetime
import re
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from app.states.registration_states import Registration
from app.keyboards.main_menu_kb import get_main_menu
from app.database.session import SessionLocal
from app.database.models import User

router = Router()


@router.message(CommandStart())
async def start_cmd(message: types.Message, state: FSMContext):
    await message.answer(
        "✨ Приветствую, путник света!\n"
        "Я — Агневидца. Чтобы подобрать тебе свечу силы, поведай своё имя."
    )
    await state.set_state(Registration.enter_name)


@router.message(Registration.enter_name)
async def get_name(message: types.Message, state: FSMContext):
    name = message.text.strip()
    if not name.isalpha():
        await message.answer("Имя должно содержать только буквы. Попробуй ещё раз 🌸")
        return
    await state.update_data(name=name)
    await state.set_state(Registration.enter_birthdate)
    await message.answer("📅 Теперь напиши дату своего рождения в формате ДД.ММ.ГГГГ")


@router.message(Registration.enter_birthdate)
async def get_birthdate(message: types.Message, state: FSMContext):
    birthdate_text = message.text.strip()
    try:
        birthdate = datetime.strptime(birthdate_text, "%d.%m.%Y").date()
    except ValueError:
        await message.answer("❌ Неверный формат даты. Введи в формате ДД.ММ.ГГГГ 🌙")
        return

    await state.update_data(birthdate=birthdate)
    await state.set_state(Registration.enter_city)
    await message.answer("🏙 Укажи свой город рождения:")


@router.message(Registration.enter_city)
async def get_city(message: types.Message, state: FSMContext):
    city = message.text.strip()
    if len(city) < 2:
        await message.answer("❌ Название города слишком короткое, попробуй снова.")
        return
    await state.update_data(city=city)

    data = await state.get_data()
    name, birthdate, city = data["name"], data["birthdate"], data["city"]

    await message.answer(
        f"🌕 Проверь данные:\n\n"
        f"Имя: <b>{name}</b>\n"
        f"Дата рождения: <b>{birthdate.strftime('%d.%m.%Y')}</b>\n"
        f"Город: <b>{city}</b>\n\n"
        f"Если всё верно, напиши <b>Да</b>, если хочешь изменить — <b>Нет</b>.",
        parse_mode="HTML"
    )
    await state.set_state(Registration.confirm_data)


@router.message(Registration.confirm_data)
async def confirm_data(message: types.Message, state: FSMContext):
    text = message.text.strip().lower()

    if text in ["да", "✅", "верно"]:
        data = await state.get_data()

        with SessionLocal() as db:
            user = User(
                telegram_id=str(message.from_user.id),
                telegram_username=message.from_user.username,
                created_at=datetime.utcnow(),
            )
            db.add(user)
            db.commit()

        await state.clear()
        await message.answer(
            f"🌟 Благодарю, <b>{data['name']}</b>!\n"
            f"Регистрация завершена. Добро пожаловать в храм свечей Candels 🔥",
            parse_mode="HTML",
            reply_markup=get_main_menu()
        )

    elif text in ["нет", "✏️"]:
        await message.answer("💫 Хорошо, начнём сначала. Как твоё имя?")
        await state.set_state(Registration.enter_name)

    else:
        await message.answer("Пожалуйста, ответь <b>Да</b> или <b>Нет</b>.", parse_mode="HTML")
