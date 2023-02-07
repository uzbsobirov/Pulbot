from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

recieve = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="To'landi ✅", callback_data='tolandi')
        ],
        [
            InlineKeyboardButton(text="Bekor qilish ❌", callback_data='bekorqilish')
        ]
    ]
)