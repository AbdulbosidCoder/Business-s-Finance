
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

contact = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text="📞Поделиться контактом", request_contact=True),
        ]
    ],
    resize_keyboard=True
)
