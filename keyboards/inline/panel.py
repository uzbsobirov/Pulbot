from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

control_balans = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="➕ Pul qo'shish", callback_data='qoshish'),
            InlineKeyboardButton(text="➖ Pul ayirish", callback_data='ayirish')
        ],
        [
            InlineKeyboardButton(text="🚷 Bloklash", callback_data='bloklash')
        ]
    ]
)

mainsettings = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Qo'llanma 📄", callback_data='qollanma'),
            InlineKeyboardButton(text="To'lovlar tarixi 🧾", callback_data='tolovtarix')
        ],
        [
            InlineKeyboardButton(text="👤 Admin useri", callback_data='adminuser')
        ],
        [
            InlineKeyboardButton(text="💸 Minimal summa", callback_data='minsum'),
            InlineKeyboardButton(text="💸 Taklif summa", callback_data='taklifsumma')
        ]
    ]
)