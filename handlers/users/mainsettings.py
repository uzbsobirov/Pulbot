from loader import dp, db, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from data.config import ADMINS
from keyboards.inline.panel import mainsettings
from states.admin import *

@dp.message_handler(text="⚙️ Asosiy sozlamalar", state='*', user_id=ADMINS[0])
async def main_settings(message: types.Message, state: FSMContext):
    await message.answer(text="<b>️ Asosiy sozlamalar</b> bo'limiga xush kelibsiz", reply_markup=mainsettings)
    await state.finish()

@dp.callback_query_handler(text="tolovtarix", state='*')
async def tolov_tarix(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    text = "<code>To'lovlar tarixi 🧾</code> <b>knopkasi uchun kanallar usernasini yuboring\n</b>"
    text += "<b>To'lovlar kanali linkini yuboring</b>\n\n"
    text += "<b>(P/s)Bu foydalanuvchiga qilgan to'lovlaringizni obunachilarga ko'rsatish uchun kerak</b>"
    await call.message.answer(text=text)
    await PayHistory.channel.set()

@dp.message_handler(state=PayHistory.channel)
async def state_channel(message: types.Message, state: FSMContext):
    text = message.text
    await state.update_data(
        {'channel': text}
    )
    await message.answer("Yaxshi, endi izohlar uchun guruh linkini yuboring")
    await PayHistory.group.set()

@dp.message_handler(state=PayHistory.group)
async def state_group(message: types.Message, state: FSMContext):
    text = message.text
    data = await state.get_data()
    chennel = data.get('channel')
    datas = f"{chennel}, {text}"
    await db.update_admin_tolov_tarix(tolovtarix=datas, id=1)
    await message.answer("<b>Kanal va Guruh bazaga qo'shildi✅</b>")
    await state.finish()

# Write handler for set `Manual`
@dp.callback_query_handler(text="qollanma", state='*')
async def qollanma_manual(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("<b>Qo'llanma uchun matn yuboring</b>")
    await Manual.text.set()

@dp.message_handler(state=Manual.text)
async def state_manual(message: types.Message, state: FSMContext):
    text = message.text
    await db.update_admin_qollanma(qollanma=text, id=1)
    await message.answer("Qo'llanma matni bazaga saqlandi✅")
    await state.finish()


# This handler set to admin or developer's username
@dp.callback_query_handler(text="adminuser", state='*')
async def admin_user(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(text="@ beligisiz <b>username</b>ni kiriting")
    await AdminUser.username.set()

@dp.message_handler(state=AdminUser.username)
async def state_username(message: types.Message, state: FSMContext):
    text = message.text
    await db.update_admin_username(adminuser=text, id=1)
    await message.answer("Admin usernamesi bazaga saqlandi✅")
    await state.finish()


# This handler to set `minimalsumma`
@dp.callback_query_handler(text="minsum", state='*')
async def pul_qoshish(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(text="<b>Minimal summa</b> uchun son yuboring\n\n"
    "<b><code>Minimal summa</code> -- bu foydalanuvchi botdan eng kam miqdorda pul chiqara olishi,"
    " yani foydalanuvchining balansidagi pul malum miqdordan kam bo'lsa foydalanuvchi pulni chiqara olmaydi!!!</b>")
    await MinSum.summa.set()

@dp.message_handler(state=MinSum.summa)
async def state_sum(message: types.Message, state: FSMContext):
    summa = message.text
    if summa.isdigit():
        await db.update_panel_min_sum(minimalsumma=int(summa), id=1)
        await bot.send_message(chat_id=ADMINS[0], text=f"<code>Minimal summa</code> saqlandi, uning qiymati -- {summa}")
        await state.finish()
    else:
        await bot.send_message(chat_id=ADMINS[0], text="<code>Minimal summa</code> faqat sonlardan tashkil topgan "
                                                       "bo'lishi kerak\n\nBoshqattan kiriting")
        await MinSum.summa.set()

# This handler to set `minimalsumma`
@dp.callback_query_handler(text="taklifsumma", state='*')
async def pul_qoshish(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(text="<b>Taklif summa</b> uchun son yuboring\n\n"
    "<b><code>Taklif summa</code> -- bu foydalanuvchi har bir taklif qilgan do'sti uchun pul miqdori</b>")
    await TaklifSumma.summa.set()

@dp.message_handler(state=TaklifSumma.summa)
async def state_sum(message: types.Message, state: FSMContext):
    summa = message.text
    if summa.isdigit():
        await db.update_panel_taklif_sum(taklifsumma=int(summa), id=1)
        await bot.send_message(chat_id=ADMINS[0], text=f"<code>Taklif summa</code> saqlandi, uning qiymati -- {summa}")
        await state.finish()
    else:
        await bot.send_message(chat_id=ADMINS[0], text="<code>Taklif summa</code> faqat sonlardan tashkil topgan "
                                                       "bo'lishi kerak\n\nBoshqattan kiriting")
        await TaklifSumma.summa.set()

# This handler send message to user
@dp.callback_query_handler(text="xabaryuborish", state='*')
async def admin_user(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    user = call.message.text.split(': ')[2][:10]
    await call.message.answer(text="<b>Foydalanuvchiga yubormoqchi bo'lgan xabaringizni yuboring!</b>")
    await state.update_data(
        {'user': user}
    )
    await SendMessage.message.set()

@dp.message_handler(state=SendMessage.message)
async def state_message(message: types.Message, state: FSMContext):
    msg = message.text
    data = await state.get_data()
    user = data.get('user')
    try:
        await bot.send_message(chat_id=int(user), text=msg)
        await bot.send_message(chat_id=ADMINS[0], text="Xabar foydalanuvchiga  muvaffaqqiyatli yuborildi✅")
        await state.finish()
    except:
        await bot.send_message(chat_id=ADMINS[0], text="Xabar foydalanuvchiga yuborilmadi❌")
        await state.finish()
