import re
from loader import db, dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from keyboards.inline.balance import balance, pulyechish, cancel
from keyboards.inline.recieve import recieve
from keyboards.default.main import main
from states.hisobraqam import Hisobraqam

# Handler for `Pul yechish 💳`
@dp.message_handler(text="Pul yechish 💳", state='*')
async def pulishlash(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    # Agar foydalanuvchi `Ban` bazasida bo'lsa
    try:
        ban_user = await db.select_one_ban_user(user_id=user_id)
        id = ban_user[0][0]
        await message.answer(text="<b>Siz botdan bloklangansiz</b>", reply_markup=ReplyKeyboardRemove())
        await state.finish()
    except IndexError:
        # user = await db.select_one_users(user_id=user_id)
        user = await db.select_one_users(user_id=user_id)
        phone = user[0][5]
        text = f"<b>Pulni <code>{phone}</code> raqamiga yechib olishni istaysizmi?\n\nUnda pastdagi «Roziman ✅» tugmasini bosing👇</b>"
        await message.reply(text=text, reply_markup=pulyechish)
        await state.finish()