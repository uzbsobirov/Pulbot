import asyncio
import types

from loader import db, dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from data.config import ADMINS
from states.reklama import Reklama
from keyboards.inline.reklama import typesads

# Handler for `🗞 Reklama yuborish`
@dp.message_handler(text="🗞 Reklama yuborish", state='*', user_id=ADMINS[0])
async def pulishlash(message: types.Message, state: FSMContext):
    await message.answer(text="Qanday reklama turidan foydalanmoqchisiz?", reply_markup=typesads)
    await state.finish()

# Suratli reklama yuborish
@dp.callback_query_handler(text="image", state="*")
async def textli(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("Reklama suratini yuboring📤")
    await Reklama.image.set()

# Rasm yuborda uning id sini olamiz
@dp.message_handler(content_types=['photo'], state=Reklama.image)
async def sendadstextli(message: types.Message, state: FSMContext):
    await message.answer("Yaxshi endi reklama textini yuboring📤")
    file_id = message['photo'][0]['file_id']
    # Rasm id sini statega saqlaymiz
    await state.update_data(
        {'file_id': file_id}
    )
    await Reklama.image_text.set()

# Rasm uchun caption olamiz va userlarga yuboramiz
@dp.message_handler(state=Reklama.image_text)
async def image_with_text(message: types.Message, state: FSMContext):
    # Foydalanuvchilarni select qilib olamiz
    users = await db.select_all_users()

    text = message.text
    data = await state.get_data()
    file_id = data.get('file_id')
    # Agar foydalanuvchi botni blok qilgan bo'lsa try, except ishlatamiz
    try:
        for user in users:
            user_id = user[3]
            await bot.send_photo(chat_id=user_id, caption=text, photo=file_id)
            await asyncio.sleep(0.05)
    except Exception as error:
        print(error)
    await state.finish()

# Oddiy text li reklama uchun
@dp.callback_query_handler(text="text", state="*")
async def textli(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("Reklama textini yuboring📤")
    await Reklama.text.set()

@dp.message_handler(state=Reklama.text)
async def reklama_text(message: types.Message, state: FSMContext):
    text = message.text
    # Foydalanuvchilarni select qilib olamiz
    users = await db.select_all_users()

    # Agar foydalanuvchi botni blok qilgan bo'lsa try, except ishlatamiz
    try:
        for user in users:
            user_id = user[3]
            await bot.send_message(chat_id=user_id, text=text)
            await asyncio.sleep(0.05)
    except Exception as error:
        print(error)
    await state.finish()


# Video reklama uchun
@dp.callback_query_handler(text="video", state="*")
async def videofunc(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("Reklama videosini yuboring📤")
    await Reklama.video.set()

@dp.message_handler(content_types=['video'], state=Reklama.video)
async def video_wtih_text(message: types.Message, state: FSMContext):
    await message.answer("Yaxshi endi reklama textini yuboring📤")
    file_id = message['video']['file_id']
    await state.update_data(
        {
            "file_id": file_id
        }
    )
    await Reklama.video_text.set()
@dp.message_handler(state=Reklama.video_text)
async def videoni_text(message: types.Message, state: FSMContext):
    text = message.text
    users = await db.select_all_users()

    data = await state.get_data()
    file_id = data.get('file_id')
    # Agar foydalanuvchi botni blok qilgan bo'lsa try, except ishlatamiz
    try:
        for user in users:
            user_id = user[3]
            await bot.send_video(chat_id=user_id, caption=text, video=file_id)
            await asyncio.sleep(0.05)
    except Exception as error:
        print(error)
    await state.finish()