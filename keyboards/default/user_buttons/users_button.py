from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

users_button = ReplyKeyboardMarkup(
    keyboard =[
        [
            KeyboardButton(text="Create Product"),
            KeyboardButton(text="Add Product"),
        ],
        [
            KeyboardButton(text="Get product info")
        ],
        [
            KeyboardButton(text="Delete Product"),
            KeyboardButton(text="Sell Product")
        ],
        [

            KeyboardButton(text="Change Product")
        ]
    ],
    resize_keyboard=True
)


