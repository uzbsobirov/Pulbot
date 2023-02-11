import re
import asyncpg
from loader import dp, bot, db
from aiogram import types
from keyboards.default.main import main
from data.config import CHANNELS, ADMINS
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
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
        if status is not True:
            final_status *= False
            result.insert(InlineKeyboardButton(text=f"❌ {channel.title}", url=invite_link))
    result.add(InlineKeyboardButton(text="✅ Obunani tekshirish", callback_data='check_subs'))
    
    if final_status:
        await db.update_user_subs(issubs='true', user_id=call.from_user.id)
        await call.message.delete()
        text = "<b>Telefon raqamingizni yuboring. ❗️\n\nRaqamni yuborish uchun pastdagi «Raqamni yuborish 📞» tugmasini bosing👇</b>"
        await call.message.answer(text=text, reply_markup=kontakt)
        await Starting.phone.set()

        # Foydalananuvchi telefon raqamini olish uchun handler
        @dp.message_handler(content_types=types.ContentTypes.CONTACT, state=Starting.phone)
        async def phone_number(message: types.Message, state: FSMContext):
            user_id = message.from_user.id
            phone = message.contact.phone_number

            if (len(phone) == 13 or len(phone) == 12) and (phone.startswith('+998') or phone.startswith('998')):
                save = await db.update_user_phone(phone=phone, user_id=message.from_user.id)
                user = await db.select_one_users(user_id=user_id)
                args = user[0][7]
                if args:
                    await message.answer("<b>Telefon raqamingiz muvaffaqiyatli kiritildi. ✅</b>", reply_markup=main)
                    await db.update_count(user_id=args)
                    await db.update_balance_count(user_id=args)
                    await bot.send_message(chat_id=args, text="<b>Sizning hisobingizga 350 so'm qo'shildi✅</b>")
                    await state.finish()

                else:
                    await message.answer("<b>Telefon raqamingiz muvaffaqiyatli kiritildi. ✅</b>", reply_markup=main)
                    await state.finish()
            else:
                # Agar user malumoti bazada bo'lsa
                try:
                    await message.answer("<b>Siz bloklandingiz. Botdan faqat O'zbekiston fuqarolari foydalanishi mumkin❗️</b>", reply_markup=ReplyKeyboardRemove())
                    ban = await db.add_ban_user(user_id=message.from_user.id, phone=phone)
                    await state.finish()
                except asyncpg.exceptions.UniqueViolationError:
                    await message.answer("<b>Siz bloklandingiz. Botdan faqat O'zbekiston fuqarolari foydalanishi mumkin❗️</b>", reply_markup=ReplyKeyboardRemove())
                    await state.finish()
    else:
        await call.message.delete()
        await call.message.answer(f"<b>❌ Siz ba'zi kanallarimizdan chiqib ketdingiz\n\nIltimos qaytadan kanalga obuna bo'ling va chiqib ketmang ❗️\n\nAks holda konkursimizdan chetlatilasiz 😣</b>", disable_web_page_preview=True, reply_markup=result)