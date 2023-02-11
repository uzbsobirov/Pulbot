from loader import db, dp
from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.message_handler(text="To'lovlar tarixi 🧾", state='*')
async def pay_history(message: types.Message, state: FSMContext):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton(text="Kanalga kirish 🧾", url='https://t.me/+T_uMxOQR-Kg4YzIy'))
    markup.add(types.InlineKeyboardButton(text="Izohlar 📝", url='https://t.me/+T_uMxOQR-Kg4YzIy'))
    text = "<b>Botimiz haqiqatdan ham to'lab beradi. ✅</b>\n\n<i>Quyidagi kanal orqali to'lovlar tarixini kuzatib borishingiz mumkin👇\nhttps://t.me/+T_uMxOQR-Kg4YzIy</i>"
    await message.reply(text=text, reply_markup=markup, disable_web_page_preview=True)