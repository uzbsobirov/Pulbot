from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

control_balans = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="➕ Pul qo'shish", callback_data='qoshish'),
            InlineKeyboardButton(text="➖ Pul ayirish", callback_data='ayirish')
        ]
    ]
)