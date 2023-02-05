from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Pul ishlash 💸")],
        [
            KeyboardButton(text="Balans 💰"),
            KeyboardButton(text="Pul yechish 💳")
        ],
        [KeyboardButton(text="To'lovlar tarixi 🧾")],
        [
            KeyboardButton(text="Qo'llanma 📄"),
            KeyboardButton(text="Top 📊")
        ]
    ], resize_keyboard=True, one_time_keyboard=True
)