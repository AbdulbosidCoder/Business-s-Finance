from aiogram import types, F
from loader import db, dp, bot
from handlers.models.user import User
from aiogram.fsm.context import FSMContext
from states.user_state import UserCreateStates
from keyboards.default.admin_buttons.users_control import user_control

data = {}

@dp.message(F.text == "Foydalanuvchi Qoshish")
async def create_user(message: types.Message, state: FSMContext):
    await message.answer(text="Please enter username: ")
    await state.set_state(UserCreateStates.username)


@dp.message(UserCreateStates.username)
async def get_username(message: types.Message, state: FSMContext):
    data["username"] = message.text
    if db.find_user_by_username(message.text):
        await message.answer("Already exists")
        return
    await message.answer(text="Please enter password: ")
    await state.set_state(UserCreateStates.password)


@dp.message(UserCreateStates.password)
async def create_password(message: types.Message, state: FSMContext):
    data["password"] = message.text
    await message.answer("Please enter phone number : ")
    await state.set_state(UserCreateStates.phone)


@dp.message(UserCreateStates.phone)
async def insert_phone(message: types.Message, state: FSMContext):
    if message.text.startswith("+998"):
        data["phone"] = message.text[1:]
        data["telegram_id"] = message.text
        user = User(**data)
        await message.answer("User successfully created", reply_markup=user_control)
        user.save(db)
    else:
        await message.answer("Please enter full phone number (+998) : ")
        return



#
# @dp.message(F.text == "Foydalanuvchi O'chirish")
# async def delete_user(message: types.Message, state: FSMContext):
#
#     await message.answer(text="Please choose user  ")
#
# @dp.message()
# async def