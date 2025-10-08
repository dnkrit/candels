from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from app.states.registration_states import Registration
from app.keyboards.main_menu_kb import get_main_menu
from app.database.session import SessionLocal
from app.database.models import User

router = Router()

# === Шаг 1. Старт регистрации ===
@router.message(Command("start"))
async def start_registration(message: types.Message, state: FSMContext):
    """Начало регистрации"""
    await state.set_state(Registration.enter_name)
    await message.answer("Привет! ✨ Я Агневидца.\nКак твоё имя, путник света?")

# === Шаг 2. Имя ===
@router.message(Registration.enter_name)
async def get_name(message: types.Message, state: FSMContext):
    name = message.text.strip()
    await state.update_data(name=name)
    await state.set_state(Registration.enter_birthdate)
    await message.answer("Запомнила 🌙\nТеперь напиши дату рождения в формате ДД.ММ.ГГГГ:")

# === Шаг 3. Дата рождения ===
@router.message(Registration.enter_birthdate)
async def get_birthdate(message: types.Message, state: FSMContext):
    birthdate = message.text.strip()
    await state.update_data(birthdate=birthdate)
    await state.set_state(Registration.enter_city)
    await message.answer("Отлично 🔮\nТеперь город рождения:")

# === Шаг 4. Город рождения ===
@router.message(Registration.enter_city)
async def get_city(message: types.Message, state: FSMContext):
    city = message.text.strip()
    data = await state.update_data(city=city)

    text = (
        f"✨ Проверим твои данные:\n"
        f"Имя: {data['name']}\n"
        f"Дата рождения: {data['birthdate']}\n"
        f"Город: {data['city']}\n\n"
        "Если всё верно — напиши ✅ или «Да».\n"
        "Если нужно изменить — напиши ✏️ или «Нет»."
    )

    await state.set_state(Registration.confirm_data)
    await message.answer(text)

# === Шаг 5. Подтверждение ===
@router.message(Registration.confirm_data)
async def confirm_data(message: types.Message, state: FSMContext):
    text = message.text.lower().strip()

    if text in ["✅", "да", "верно", "подтверждаю"]:
        data = await state.get_data()

        with SessionLocal() as db:
            user = User(
                first_name=data["name"],
                birth_date=data["birthdate"],
                birth_place=data["city"]
            )
            db.add(user)
            db.commit()

        # Показываем главное меню (ReplyKeyboard)
        await message.answer(
            "Добро пожаловать, маг света 🔥\n"
            "Выбери раздел, с которого начнем:",
            reply_markup=get_main_menu()
        )

        await state.clear()

    elif text in ["✏️", "нет", "изменить"]:
        await state.set_state(Registration.enter_name)
        await message.answer("Хорошо, начнем заново ✨\nКак твоё имя?")

    else:
        await message.answer("Пожалуйста, ответь «Да» или «Нет» (или выбери символы ✅ / ✏️).")
