from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

balance = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Pulni yechish💳", callback_data='pulniyechish')
        ],
        [
            InlineKeyboardButton(text="Hisob raqamni kiritish📱", callback_data='hisobraqam')
        ]
    ]
)


pulyechish = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Roziman ✅", callback_data='agree')
        ]
    ]
)