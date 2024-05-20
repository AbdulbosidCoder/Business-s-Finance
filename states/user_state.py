from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    username = State()
    password = State()
    phone = State()

class UserCreateStates(StatesGroup):
    username = State()
    password = State()
    phone = State()