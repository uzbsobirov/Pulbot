import asyncpg
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.deep_linking import get_start_link

from data.config import ADMINS, CHANNELS
from keyboards.default.main import main, main_admin
from loader import dp, db, bot
from states.starting import Starting


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    full_name = message.from_user.full_name
    username = message.from_user.username
    user_id = message.from_user.id
    referal_link = await get_start_link(str(user_id))
    args = message.get_args()

    # Foydalanuvchi bazada bo'lsa faqat admin xabar beramiz aks xolda bazafa qo'shib keyin adminga xabar beramiz
    try:
        # `args` ni tekshiramiz
        if args == '':
            user = await db.add_user(
                user_id=user_id,
                full_name=full_name,
                username=username,
                issubs='false',
                referal_link=referal_link,
                parent_id=None,
                count=0,
                balance=0,
                wallet=None
            )
            await db.add_user_to_panel()
            await db.add_sponsor_test(channel='@blogca')
        else:
            user = await db.add_user(
                user_id=user_id,
                full_name=full_name,
                username=username,
                issubs='false',
                referal_link=referal_link,
                parent_id=int(args),
                count=0,
                balance=0,
                wallet=None
            )
            await db.add_user_to_panel()
            await db.add_sponsor_test(channel='@blogca')
        # ADMINGA xabar beramiz
        count = await db.count_users()
        msg = f"{full_name} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
        await bot.send_message(chat_id=ADMINS[0], text=msg)
    except asyncpg.exceptions.UniqueViolationError:
        # user = await db.select_user(telegram_id=message.from_user.id)
        await bot.send_message(chat_id=ADMINS[0], text=f"{full_name} bazaga oldin qo'shilgan")

    # Majburiy obuna uchun kanal bo'lsa obuna bo'lishi so'raymiz aks xolda yo'q
    sponsor_channels = await db.select_row_panel()
    sponsor = sponsor_channels[0][1]

    if sponsor is not None:
        # User malumotlarini olamiz
        datas = await db.select_one_users(user_id=user_id)
        issubs = datas[0][4]
        if issubs == 'false':
            markup = InlineKeyboardMarkup(row_width=1)
            for channel in CHANNELS:
                chat = await bot.get_chat(channel)
                invite_link = await chat.export_invite_link()
                markup.insert(InlineKeyboardButton(text=chat.title, url=invite_link))
            markup.add(InlineKeyboardButton(text="✅ Obunani tekshirish", callback_data='check_subs'))

            text = f"<b>Assalomu aleykum</b>, {username}\n\nUydan chiqmasdan optimize orqali pul ishlang, "\
                   "vazifalarni bajaring va har kuni <b>70 000</b> so'mdan ortiq pul ishlang!\n\nBotdan foydalanish "\
                   "uchun quyidagi kanallarimizga a'zo bo'ling 👇"
            await message.answer(text=text, reply_markup=markup, disable_web_page_preview=True)
            await state.finish()
        else:
            phone = datas[0][5]
            if phone is None or phone == '' or phone == ([], {}, ()):
                # Foydalananuvchi telefon raqamini olish uchun handler
                @dp.message_handler(content_types=types.ContentTypes.CONTACT, state=Starting.phone)
                async def phone_number(message: types.Message, state: FSMContext):
                    user_id = message.from_user.id
                    phone = message.contact.phone_number
                    mention = message.from_user.get_mention(full_name, as_html=True)

                    if (len(phone) == 13 or len(phone) == 12) and (phone.startswith('+998') or phone.startswith('998')):
                        save = await db.update_user_phone(phone=phone, user_id=message.from_user.id)
                        user = await db.select_one_users(user_id=user_id)
                        args = user[0][7]
                        if args:
                            if user_id == int(ADMINS[0]):
                                await message.answer("<b>Telefon raqamingiz muvaffaqiyatli kiritildi. ✅</b>",
                                                     reply_markup=main_admin)
                                await db.update_count(user_id=args)
                                await db.update_balance_count(user_id=args)
                                await bot.send_message(chat_id=args, text=f"<b>Tabriklaymiz siz taklif qilgan "
                                    "do'stingiz {mention} botimizga a'zo bo'ldi va sizga 200 so'm taqdim etildi👏</b>")
                                await state.finish()
                            else:
                                await message.answer("<b>Telefon raqamingiz muvaffaqiyatli kiritildi. ✅</b>",
                                                     reply_markup=main)
                                await db.update_count(user_id=args)
                                await db.update_balance_count(user_id=args)
                                await bot.send_message(chat_id=args,
                                                   text=f"<b>Tabriklaymiz siz taklif qilgan do'stingiz {mention} "
                                                        "botimizga a'zo bo'ldi va sizga 200 so'm taqdim etildi👏</b>")
                                await state.finish()
                        else:
                            if user_id == int(ADMINS[0]):
                                await message.answer("<b>Telefon raqamingiz muvaffaqiyatli kiritildi. ✅</b>",
                                                     reply_markup=main_admin)
                                await state.finish()
                            else:
                                await message.answer("<b>Telefon raqamingiz muvaffaqiyatli kiritildi. ✅</b>",
                                                     reply_markup=main)
                                await state.finish()
                    else:
                        # Agar user malumoti bazada bo'lsa
                        try:
                            await message.answer("<b>Siz bloklandingiz. Botdan faqat O'zbekiston fuqarolari "
                                                 "foydalanishi mumkin❗️</b>", reply_markup=ReplyKeyboardRemove())
                            ban = await db.add_ban_user(user_id=message.from_user.id, phone=phone)
                            await state.finish()
                        except asyncpg.exceptions.UniqueViolationError:
                            await message.answer("<b>Siz bloklandingiz. Botdan faqat O'zbekiston fuqarolari "
                                                 "foydalanishi mumkin❗️</b>", reply_markup=ReplyKeyboardRemove())
                            await state.finish()
            else:
                if user_id == int(ADMINS[0]):
                    answer = f"{full_name}, siz uchun shart tayyor!\n\nBoshlash uchun «Pul ishlash» tugmasini bosing 👇"
                    await message.answer(text=answer, reply_markup=main_admin)
                    await state.finish()
                else:
                    answer = f"{full_name}, siz uchun shart tayyor!\n\nBoshlash uchun «Pul ishlash» tugmasini bosing 👇"
                    await message.answer(text=answer, reply_markup=main)
                    await state.finish()
    # else:
    #     datas = await db.select_one_users(user_id=user_id)
    #     phone = datas[0][5]
    #     if phone is None or phone == '' or phone == ([], {}, ()):
    #         # Foydalananuvchi telefon raqamini olish uchun handler
    #         @dp.message_handler(content_types=types.ContentTypes.CONTACT, state=Starting.phone)
    #         async def phone_number(message: types.Message, state: FSMContext):
    #             user_id = message.from_user.id
    #             phone = message.contact.phone_number
    #             mention = message.from_user.get_mention(full_name, as_html=True)
    #
    #             if (len(phone) == 13 or len(phone) == 12) and (phone.startswith('+998') or phone.startswith('998')):
    #                 save = await db.update_user_phone(phone=phone, user_id=message.from_user.id)
    #                 user = await db.select_one_users(user_id=user_id)
    #                 args = user[0][7]
    #                 if args:
    #                     if user_id == int(ADMINS[0]):
    #                         await message.answer("<b>Telefon raqamingiz muvaffaqiyatli kiritildi. ✅</b>",
    #                                              reply_markup=main_admin)
    #                         await db.update_count(user_id=args)
    #                         await db.update_balance_count(user_id=args)
    #                         await bot.send_message(chat_id=args,
    #                             text=f"<b>Tabriklaymiz siz taklif qilgan do'stingiz {mention} botimizga a'zo bo'ldi "
    #                                  "va sizga 200 so'm taqdim etildi👏</b>")
    #                         await state.finish()
    #                     else:
    #                         await message.answer("<b>Telefon raqamingiz muvaffaqiyatli kiritildi. ✅</b>",
    #                                              reply_markup=main)
    #                         await db.update_count(user_id=args)
    #                         await db.update_balance_count(user_id=args)
    #                         await bot.send_message(chat_id=args,
    #                                                text=f"<b>Tabriklaymiz siz taklif qilgan do'stingiz {mention} "
    #                                                     "botimizga a'zo bo'ldi va sizga 200 so'm taqdim etildi👏</b>")
    #                         await state.finish()
    #                 else:
    #                     if user_id == int(ADMINS[0]):
    #                         await message.answer("<b>Telefon raqamingiz muvaffaqiyatli kiritildi. ✅</b>",
    #                                              reply_markup=main_admin)
    #                         await state.finish()
    #                     else:
    #                         await message.answer("<b>Telefon raqamingiz muvaffaqiyatli kiritildi. ✅</b>",
    #                                              reply_markup=main)
    #                         await state.finish()
    #             else:
    #                 # Agar user malumoti bazada bo'lsa
    #                 try:
    #                     await message.answer(
    #                         "<b>Siz bloklandingiz. Botdan faqat O'zbekiston fuqarolari foydalanishi mumkin❗️</b>",
    #                         reply_markup=ReplyKeyboardRemove())
    #                     ban = await db.add_ban_user(user_id=message.from_user.id, phone=phone)
    #                     await state.finish()
    #                 except asyncpg.exceptions.UniqueViolationError:
    #                     await message.answer(
    #                         "<b>Siz bloklandingiz. Botdan faqat O'zbekiston fuqarolari foydalanishi mumkin❗️</b>",
    #                         reply_markup=ReplyKeyboardRemove())
    #                     await state.finish()
    #     else:
    #         if user_id == int(ADMINS[0]):
    #             answer = f"{full_name}, siz uchun shart tayyor!\n\nBoshlash uchun «Pul ishlash» tugmasini bosing 👇"
    #             await message.answer(text=answer, reply_markup=main_admin)
    #             await state.finish()
    #         else:
    #             answer = f"{full_name}, siz uchun shart tayyor!\n\nBoshlash uchun «Pul ishlash» tugmasini bosing 👇"
    #             await message.answer(text=answer, reply_markup=main)
    #             await state.finish()
