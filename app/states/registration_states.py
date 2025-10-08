from aiogram.fsm.state import StatesGroup, State

class Registration(StatesGroup):
    enter_name = State()
    enter_birthdate = State()
    enter_city = State()
    confirm_data = State()
