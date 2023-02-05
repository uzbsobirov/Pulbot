from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kontakt = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Raqamni yuborish 📞", request_contact=True)]
    ], resize_keyboard=True
)