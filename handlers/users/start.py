import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp, db, bot
from data.config import ADMINS, CHANNELS
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    full_name = message.from_user.full_name
    username = message.from_user.username
    user_id = message.from_user.id

    markup = InlineKeyboardMarkup(row_width=1)
    for channel in CHANNELS:
        chat = await bot.get_chat(channel)
        invite_link = await chat.export_invite_link()
        markup.insert(InlineKeyboardButton(text=chat.title, url=invite_link))
    markup.add(InlineKeyboardButton(text="✅ Obunani tekshirish", callback_data='check_subs'))

    try:
        user = await db.add_user(
            user_id=user_id,
            full_name=full_name,
            username=username,
            issubs='false'
        )                    

        # ADMINGA xabar beramiz
        count = await db.count_users()
        msg = f"@{user[2]} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
        await bot.send_message(chat_id=ADMINS[0], text=msg)
    except asyncpg.exceptions.UniqueViolationError:
        # user = await db.select_user(telegram_id=message.from_user.id)
        await bot.send_message(chat_id=ADMINS[0], text=f"@{username} bazaga oldin qo'shilgan")

    text = f"<b>Assalomu aleykum</b>, {username}\n\nUydan chiqmasdan botimiz orqali pul ishlang, vazifalarni bajaring va har kuni <b>70 000</b> so'mdan ortiq pul ishlang!\n\nBotdan foydalanish uchun quyidagi kanallarimizga a'zo bo'ling 👇"
    await message.answer(text=text, reply_markup=markup, disable_web_page_preview=True)
    await state.finish()
