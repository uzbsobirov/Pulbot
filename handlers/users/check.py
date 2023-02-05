import re
import asyncpg
from loader import dp, bot, db
from aiogram import types
from keyboards.default.main import main
from data.config import CHANNELS
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from utils.misc.subscription import check
from states.starting import Starting
from keyboards.default.contact import kontakt


# Obunani tekshirish uchun handler
@dp.callback_query_handler(text="check_subs")
async def check_user_subs(call: types.CallbackQuery, state: FSMContext):
    await call.answer("Obuna tekshirilmoqda...")
    final_status = True

    result = InlineKeyboardMarkup(row_width=1)
    
    for channel in CHANNELS:
        status = await check(user_id=call.from_user.id, channel=channel)
        channel = await bot.get_chat(channel)
        invite_link = await channel.export_invite_link()
        # if status:
        #     final_status *= status
        #     # result +=  f"✅ <b>{channel.title}</b> kanaliga obuna bo'lgansiz\n\n"
        #     result.insert(InlineKeyboardButton(text=f"✅ {channel.title}", url=invite_link))
        # Agar user bazi kanallarga obuna bo'lmagan bo'lsa u shu bosqichdan o'tadi
        if status is not True:
            final_status *= False
            result.insert(InlineKeyboardButton(text=f"❌ {channel.title}", url=invite_link))
    result.add(InlineKeyboardButton(text="✅ Obunani tekshirish", callback_data='check_subs'))
    
    if final_status:
        await call.message.delete()
        text = "<b>Telefon raqamingizni yuboring. ❗️\n\nRaqamni yuborish uchun pastdagi «Raqamni yuborish 📞» tugmasini bosing👇</b>"
        await call.message.answer(text=text, reply_markup=kontakt)
        await Starting.phone.set()

        # Foydalananuvchi telefon raqamini olish uchun handler
        @dp.message_handler(content_types=types.ContentTypes.CONTACT, state=Starting.phone)
        async def phone_number(message: types.Message, state: FSMContext):
            phone = message.contact.phone_number
            andoza = ""
        # text = f"<b>{call.from_user.full_name}, siz uchun shart tayyor!\n\nBoshlash uchun «Pul ishlash» tugmasini bosing 👇</b>"
        # await call.message.answer(text=text, reply_markup=main)
        # await state.finish()
    else:
        await call.message.delete()
        await call.message.answer(f"<b>❌ Siz ba'zi kanallarimizdan chiqib ketdingiz\n\nIltimos qaytadan kanalga obuna bo'ling va chiqib ketmang ❗️\n\nAks holda konkursimizdan chetlatilasiz 😣</b>", disable_web_page_preview=True, reply_markup=result)