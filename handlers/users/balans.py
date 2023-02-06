from loader import db, dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from keyboards.inline.balance import balance, pulyechish

# Handler for `Balans 💰`
@dp.message_handler(text="Balans 💰", state='*')
async def pulishlash(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    # Agar foydalanuvchi `Ban` bazasida bo'lsa
    try:
        ban_user = await db.select_one_ban_user(user_id=user_id)
        id = ban_user[0][0]
        await message.answer(text="<b>Siz botdan bloklangansiz</b>", reply_markup=ReplyKeyboardRemove())
        await state.finish()
    except IndexError:
        user = await db.select_one_users(user_id=user_id)
        balans = user[0][-1]
        ref_count = user[0][8]
        phone = user[0][5]
        text = f"<b>💰Hisobingiz: <code>{balans}</code> so'm\n👥Taklif qilgan do'stlaringiz: <code>{ref_count}</code> odam\n📱Hisob raqamingiz: <code>{phone}</code></b>"
        await message.reply(text=text, reply_markup=balance)
        await state.finish()

# CallbackHandler for `pulyechish`
@dp.callback_query_handler(text="pulniyechish", state='*')
async def pulni_yechish(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id

    user = await db.select_one_users(user_id=user_id)
    phone = user[0][5]
    text = f"<b>Pulni <code>{phone}</code> raqamiga yechib olishni istaysizmi?\n\nUnda pastdagi «Roziman ✅» tugmasini bosing👇</b>"
    await call.message.edit_text(text=text, reply_markup=pulyechish)
    await state.finish()

# CallbackHandler for `pulyechish`
@dp.callback_query_handler(text="agree", state='*')
async def pulni_yechish(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id

    user = await db.select_one_users(user_id=user_id)
    balans = user[0][-1]
    if balans < 100:
        await call.answer(text="Pulni olish uchun hisobingizda mablag' yetarli emas❗️\n\nPulni olish hisobingizda eng kamida 4000 so'm pul bo'lishi kerak💰", show_alert=True)
    else:
        await call.message.delete()
        await db.update_user_balance(balance=0, user_id=user_id)
        text = "<b>So'rovingizni qabul qilindi✅\n\nPul hisobingizga 10 daqiqa ichida tushadi⚡️</b>"
        await call.message.answer(text=text)
        await state.finish()