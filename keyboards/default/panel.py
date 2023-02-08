from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

panel = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="⚙️ Asosiy sozlamalar")],
        [
            KeyboardButton(text="📊 Statistika"),
            KeyboardButton(text="🗞 Reklama yuborish")
        ],
        [
            KeyboardButton(text="👤 Foydalanuvchini boshqarish")
        ],
        [
            KeyboardButton(text="◀️ Orqaga")
        ]
    ], resize_keyboard=True, one_time_keyboard=True
)