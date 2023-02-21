from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

control_balans = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="➕ Pul qo'shish", callback_data='qoshish'),
            InlineKeyboardButton(text="➖ Pul ayirish", callback_data='ayirish')
        ],
        [
            InlineKeyboardButton(text="📤 Xabar yuborish", callback_data='xabaryuborish'),
            InlineKeyboardButton(text="🚷 Bloklash", callback_data='bloklash')
        ],
        [
            InlineKeyboardButton(text="💣 Delete User", callback_data='deleteruser')
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

add_sponsor = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="➕ Kanal qo'shish", callback_data='addsponsor')
        ],
        [
            InlineKeyboardButton(text="🗑 Kanalni o'chirish", callback_data='deletesponsor')
        ]
    ]
)

sponsor_add = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="➕ Yana qo'shish", callback_data='addsponsor')
        ]
    ]
)