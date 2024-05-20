from loader import db, dp, bot
from data.config import ADMINS
from aiogram.types import Message
from handlers.models.user import User
from states.user_state import UserState
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from keyboards.default.Roles.contact import contact
from keyboards.default.admin_buttons.users_control import user_control
from keyboards.default.user_buttons.users_button import users_button


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    if str(message.from_user.id) in ADMINS:
        await message.answer("Assalomu Aleykum", reply_markup=user_control)
        await state.clear()
    elif db.get_user_by_telegra_id(message.from_user.id):
        await message.answer("Assalomu Aleykum.", reply_markup=users_button)
        await state.clear()
    else:
        await message.answer("Please enter phone number : ", reply_markup=contact)
        await state.set_state(UserState.phone)


@dp.message(UserState.phone)
async def checking_phone(message: Message, state: FSMContext):
    try:
        user_contact = message.contact.phone_number
    except:
        await message.answer("Please enter your contact", reply_markup = contact)
        return
    if user_contact.startswith("998"):
        if db.get_user_by_phone(user_contact):
            db.update_user_telegram_id_by_phone(phone=user_contact, telegram_id=message.from_user.id)
            await message.answer("<i>Assalomu Aleykum</i> \nYou have access for this functions", reply_markup=users_button)
            await state.clear()
        else:
            await message.answer("This phone number does not exist")
            return
    else:
        await message.answer("This phone number does not exist")
        return


