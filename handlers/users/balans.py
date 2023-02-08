import re
from loader import db, dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from keyboards.inline.balance import balance, pulyechish, cancel
from keyboards.inline.recieve import recieve
from keyboards.default.main import main
from states.hisobraqam import Hisobraqam

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
        balans = user[0][9]
        ref_count = user[0][8]
        wallet = user[0][10]
        phone = user[0][5]
        if wallet is not None:
            text = f"<b>💰Hisobingiz: <code>{balans}</code> so'm\n📱Hisob raqamingiz: <code>{wallet}</code></b>"
            await message.reply(text=text, reply_markup=balance)
            await state.finish()
        else:
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
async def rozilik(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    full_name = call.from_user.full_name
    user_data = call.from_user.get_mention(f"{full_name}", as_html=True)
    user = await db.select_one_users(user_id=user_id)
    balans = user[0][9]
    phone = user[0][5]
    if balans < 100:
        await call.answer(text="Pulni olish uchun hisobingizda mablag' yetarli emas❗️\n\nPulni olish hisobingizda eng kamida 4000 so'm pul bo'lishi kerak💰", show_alert=True)
    else:
        await call.message.delete()
        text = "<b>So'rovingizni qabul qilindi✅\n\nPul hisobingizga 10 daqiqa ichida shadily⚡️</b>"
        admin_text = f"<b>#RecieveRequest\n\n🆔 <code>{user_id}</code>\n👤 {user_data}\n📲 Raqam: <code>{phone}</code>\n💰 Summa: <code>{balans}</code> so'm</b>"
        await bot.send_message(chat_id=-1001628560121, text=admin_text, reply_markup=recieve)
        await call.message.answer(text=text)
        await state.finish()

# Agar foydalanuvchi adminga hisobidagi pulni chiqarish uchun so'rov yuborsa va admin uni tasdiqlasa...
@dp.callback_query_handler(text="tolandi", state='*')
async def pul_tolandi(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    # full_name = call.from_user.full_name
    user_data = call.from_user.get_mention("Pul oluvchi", as_html=True)
    data = call.message.text.split('\n')
    step1 = data[2].split(' ')
    user_id = step1[1]


    user = await db.select_one_users(user_id=int(user_id))
    balans = user[0][-2]
    phone = user[0][5]
    await db.update_user_balance(balance=0, user_id=int(user_id))
    admin_text = f"<b>#tolov\n\n👤 {user_data}\n📲 Raqam: <code>{phone}</code>\n💰 Summa: <code>{balans}</code>\n\n<i>✅ Muvaffaqiyatli o'tkazildi</i>\n\n@Puldorkubot</b>"
    await bot.send_message(chat_id=-1001828522631, text=admin_text)
    text = "Pulingiz hisobingizga o'tkazildi✅, iltimos hisobingizni tekshiring❗️"
    await bot.send_message(chat_id=user_id, text=text)
    await state.finish()


# Hisob raqam qo'shish yoki yangilash uchun handler
@dp.callback_query_handler(text="hisobraqam", state='*')
async def hisob_raqam(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    # Foydalanuvchi id sini olaman `state` orqali
    await state.update_data(
        {'user_id': user_id}
    )
    text = "<b>Pul o'tkazish kerak bo'lgan telefon raqamingizni yoki karta raqamingizni kiriting\n\nNamuna:\nTelefon raqam: <code>+998912345678</code>\nKarta raqam: <code>8600111122223333</code></b>"
    await call.message.edit_text(text=text, reply_markup=cancel)
    await Hisobraqam.hisobraqam.set()

# Foydalanuvchi habarini olish uchun state ni set qilamiz
@dp.message_handler(state=Hisobraqam.hisobraqam)
async def new_hisob_raqam(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get('user_id')
    msg = message.text

    # Agar foydalanuvchi hisob raqamga telefon raqam kiritishni xoxlasa RegEx dan foydalanamiz
    andoza1 = "(?:\+[9]{2}[8][0-9]{2}[0-9]{3}[0-9]{2}[0-9]{2})" # For startswith='99, 97, 90, 91, 94, 95'
    andoza2 = "(?:\+[9]{2}[8][7]{2}[0-9]{3}[0-9]{2}[0-9]{2})" # For startswith='77'
    andoza3 = "(?:\+[9]{2}[8][8]{2}[0-9]{3}[0-9]{2}[0-9]{2})" # For startswith='88'
    if re.match(andoza1, msg) or re.match(andoza2, msg) or re.match(andoza3, msg):
        await db.update_user_wallet(wallet=msg, user_id=user_id)
        await message.reply("Telefon raqamingiz muvaffaqiyatli kiritildi. ✅", reply_markup=main)
        await state.finish()
    elif (len(msg) == 16) and (msg.startswith("8600") or msg.startswith("9860")):
        await db.update_user_wallet(wallet=msg, user_id=user_id)
        await message.reply("Karta raqamingiz muvaffaqiyatli kiritildi. ✅", reply_markup=main)
        await state.finish()
    else:
        # Agar user kiritgan hisob raqam yaroqsiz bo'lsa `state` ni `reset` qilamiz va boshqa hisob raqam kiritishini
        #                                                                                                   so'raymiz
        text = "<b>Iltimos telefon raqamingiz yoki karta raqamingizni namunadagiday yuboring❗️\n\nNamuna (Telefon raqam uchun): <code>+998912345678</code>\nNamuna (Karta raqam uchun): <code>8600111122223333</code></b>"
        await message.reply(text=text)
        await Hisobraqam.hisobraqam.set()
