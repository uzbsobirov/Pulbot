import asyncio
import types

from loader import db, dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from data.config import ADMINS
from states.reklama import Reklama, YesNo
from keyboards.inline.reklama import typesads
from keyboards.inline.adver import yes_no, check_ha


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
    rasm_txt = message.text

    await state.update_data(
        {'rasm_txt': rasm_txt}
    )

    await message.answer(text="Tugma qo'shamizmi?", reply_markup=yes_no)
    await YesNo.image_choose.set()

@dp.callback_query_handler(state=YesNo.image_choose)
async def state_video_ha(call: types.CallbackQuery, state: FSMContext):

    # Foydalanuvchilarni select qilib olamiz
    users = await db.select_all_users()

    if call.data == 'check_yoq':
        data = await state.get_data()
        file_id = data.get('file_id')
        video_txt = data.get('video_txt')
        # Agar foydalanuvchi botni blok qilgan bo'lsa try, except ishlatamiz
        try:
            for user in users:
                user_id = user[3]
                await bot.send_photo(chat_id=user_id, caption=video_txt, photo=file_id)
                await asyncio.sleep(0.05)
        except Exception as error:
            print(error)
        await state.finish()
    else:
        await call.message.delete()
        await call.message.answer(text="Tugma uchun text va link yuboring! <code>Text</code>+<code>Link</code>\n\n"
                                       "Exm: <b>Kanalga o'tish+https://t.me/blogca</b>")
        await YesNo.image_ha.set()

@dp.message_handler(state=YesNo.image_ha)
async def state_yes_btn(message: types.Message, state: FSMContext):
    data = await state.get_data()
    rasm_txt = data.get('rasm_txt')
    file_id = data.get('file_id')

    text = message.text
    txt = text.split('+')[0]
    url = text.split('+')[1]

    # Foydalanuvchilarni select qilib olamiz
    users = await db.select_all_users()

    # Agar foydalanuvchi botni blok qilgan bo'lsa try, except ishlatamiz
    try:
        for user in users:
            user_id = user[3]
            await bot.send_photo(chat_id=user_id, photo=file_id, caption=rasm_txt, reply_markup=check_ha(text=txt,
                                                                                                         url=url))
            await asyncio.sleep(0.05)
        await bot.send_message(chat_id=message.chat.id, text="Xabar foydalanuvchilarga muvaffaqqiyali yuborildi")
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

    await state.update_data(
        {'text': text}
    )

    await message.answer(text="Tugma qo'shamizmi?", reply_markup=yes_no)
    await YesNo.choose.set()


@dp.callback_query_handler(state=YesNo.choose)
async def yes_no_choose(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get('text')


    # Foydalanuvchilarni select qilib olamiz
    users = await db.select_all_users()

    if call.data == 'check_yoq':
        await call.message.delete()
        # Agar foydalanuvchi botni blok qilgan bo'lsa try, except ishlatamiz
        try:
            for user in users:
                user_id = user[3]
                await bot.send_message(chat_id=user_id, text=text)
                await asyncio.sleep(0.05)
        except Exception as error:
            print(error)
        await state.finish()
    else:
        await call.message.delete()
        await call.message.answer(text="Tugma uchun text va link yuboring! <code>Text</code>+<code>Link</code>\n\n"
                                       "Exm: <b>Kanalga o'tish+https://t.me/blogca</b>")
        await YesNo.btn_ha.set()

@dp.message_handler(state=YesNo.btn_ha)
async def state_yes_btn(message: types.Message, state: FSMContext):
    data = await state.get_data()
    reklama_text = data.get('text')

    text = message.text
    txt = text.split('+')[0]
    url = text.split('+')[1]

    # Foydalanuvchilarni select qilib olamiz
    users = await db.select_all_users()

    # Agar foydalanuvchi botni blok qilgan bo'lsa try, except ishlatamiz
    try:
        for user in users:
            user_id = user[3]
            await bot.send_message(chat_id=user_id, text=reklama_text, reply_markup=check_ha(text=txt, url=url))
            await asyncio.sleep(0.05)
        await bot.send_message(chat_id=message.chat.id, text="Xabar foydalanuvchilarga muvaffaqqiyali yuborildi")
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
            "video_id": file_id
        }
    )
    await Reklama.video_text.set()
@dp.message_handler(state=Reklama.video_text)
async def videoni_text(message: types.Message, state: FSMContext):
    video_text = message.text

    await state.update_data(
        {'video_text': video_text}
    )

    await message.answer(text="Tugma qo'shamizmi?", reply_markup=yes_no)
    await YesNo.video_choose.set()

@dp.callback_query_handler(state=YesNo.video_choose)
async def state_video_choose(call: types.CallbackQuery, state: FSMContext):

    if call.data == 'check_yoq':
        data = await state.get_data()
        file_id = data.get('video_id')
        video_text = data.get('video_text')

        # Foydalanuvchilarni select qilib olamiz
        users = await db.select_all_users()

        # Agar foydalanuvchi botni blok qilgan bo'lsa try, except ishlatamiz
        try:
            for user in users:
                user_id = user[3]
                await bot.send_video(chat_id=user_id, caption=video_text, video=file_id)
                await asyncio.sleep(0.05)
        except Exception as error:
            print(error)
        await state.finish()
    else:
        await call.message.delete()
        await call.message.answer(text="Tugma uchun text va link yuboring! <code>Text</code>+<code>Link</code>\n\n"
                                       "Exm: <b>Kanalga o'tish+https://t.me/blogca</b>")
        await YesNo.video_ha.set()


@dp.message_handler(state=YesNo.video_ha)
async def state_yes_btn(message: types.Message, state: FSMContext):
    data = await state.get_data()
    file_id = data.get('video_id')
    video_text = data.get('video_text')

    text = message.text
    txt = text.split('+')[0]
    url = text.split('+')[1]

    # Foydalanuvchilarni select qilib olamiz
    users = await db.select_all_users()

    # Agar foydalanuvchi botni blok qilgan bo'lsa try, except ishlatamiz
    try:
        for user in users:
            user_id = user[3]
            await bot.send_video(chat_id=user_id, video=file_id, caption=video_text, reply_markup=check_ha(text=txt,
                                                                                                        url=url))
            await asyncio.sleep(0.05)
        await bot.send_message(chat_id=message.chat.id, text="Xabar foydalanuvchilarga muvaffaqqiyali yuborildi")
    except Exception as error:
        print(error)
    await state.finish()
