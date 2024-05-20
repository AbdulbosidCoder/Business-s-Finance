from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

user_control = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text="Foydalanuvchi Qoshish"),
            KeyboardButton(text="Foydalanuvchi Ochirish"),
        ],
        [
            KeyboardButton(text="Foydalanuvchini malumotlarini ozgartirish")
        ],
    ],
    resize_keyboard=True
)


