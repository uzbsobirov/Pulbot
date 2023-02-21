import datetime
from loader import db, dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from data.config import ADMINS
from states.control import Control
from keyboards.inline.panel import control_balans

# Handler for `👤 Foydalanuvchini boshqarish`
@dp.message_handler(text="👤 Foydalanuvchini boshqarish", state='*', user_id=ADMINS[0])
async def control_user(message: types.Message, state: FSMContext):
    await message.answer(text="<b>Foydalanuvchi id raqamini kiriting</b>")
    await Control.control.set()

@dp.message_handler(state=Control.control)
async def controluser(message: types.Message, state: FSMContext):
    user_id = message.text

    if user_id.isdigit():
        try:
            user = await db.select_one_users(user_id=int(user_id))
            id = user[0][0]
            full_name = user[0][1]
            username = user[0][2]
            userid = user[0][3]
            issubs = user[0][4]
            phone = user[0][5]
            referal_link = user[0][6]
            parent_id = user[0][7]
            count = user[0][8]
            balance = user[0][9]
            wallet = user[0][10]

            user_data = f"<a href='tg://user?id={userid}'>{full_name}</a>"

            # bazi malumotlar bosh emasligini tekshiramiz
            if username:
                text = f"<b>🔑: <code>{id}</code>\n\n🆔: <code>{userid}</code>\n" \
                       f"👤: {user_data} | @{username}\n" \
                       f"Deeplink🔗: <i>{referal_link}</i>\nTelefon raqam📲: <i>{phone}</i>\n" \
                       f"Kanallarga a'zo〽️: <i>{issubs}</i>\n" \
                       f"Parent id👨🏻‍🦳: <i>{parent_id}</i>\nTaklif qilgan odamlari🔢: <i>{count}</i>\n" \
                       f"Balans💰: {balance} so'm\n" \
                       f"Hisob raqam💳: <i>{wallet}</i></b>"
                await message.answer(text=text, disable_web_page_preview=True, reply_markup=control_balans)
                await state.finish()
            else:
                text = f"<b>🔑: <code>{id}</code>\n\n🆔: <code>{userid}</code>\n" \
                       f"👤: {user_data}\n" \
                       f"Deeplink🔗: <i>{referal_link}</i>\nTelefon raqam📲: <i>{phone}</i>\n" \
                       f"Kanallarga a'zo〽️: <i>{issubs}</i>\n" \
                       f"Parent id👨🏻‍🦳: <i>{parent_id}</i>\nTaklif qilgan odamlari🔢: <i>{count}</i>\n"\
                       f"Balans💰: {balance}\n" \
                       f"Hisob raqam💳: <i>{wallet}</i></b>"
                await message.answer(text=text, disable_web_page_preview=True, reply_markup=control_balans)
                await state.finish()

        except:
            await message.answer(text="Bunday iddagi foydalanuvchi topilmadi😞\n\nBoshqa id kiriting")
            await Control.control.set()

    else:
        await message.answer(text="Iltimos, faqat sonlardan foydalaning❗️")
        await Control.control.set()

# Foydalanuvchi balansiga pul qoshish uchun
@dp.callback_query_handler(text="qoshish", state='*')
async def pul_qoshish(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text="<b>Foydalanuvchi balansiga nech pul qo'shmoqchisiz?</b>")
    user_id = call.message.text.split('\n')[2].split(': ')[1]
    await state.update_data(
        {'user_id': user_id}
    )
    await Control.add.set()

@dp.message_handler(state=Control.add)
async def state_add(message: types.Message, state: FSMContext):
    text = message.text
    data = await state.get_data()
    user_id = data.get('user_id')

    await db.add_user_balance(user_id=int(user_id), miqdor=int(text))
    await message.answer(text=f"<code>{user_id}</code> - dagi foydalanuvchining balansiga <code>{text}</code> "
                              "so'm qo'shildi✅")
    await state.finish()

# Foydalanuvchi balansidan pul olish  uchun
@dp.callback_query_handler(text="ayirish", state='*')
async def pul_qoshish(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text="<b>Foydalanuvchi balansiga nech pul olmoqchisiz?</b>")
    user_id = call.message.text.split('\n')[2].split(': ')[1]
    await state.update_data(
        {'user_id': user_id}
    )
    await Control.subtraction.set()

@dp.message_handler(state=Control.subtraction)
async def state_add(message: types.Message, state: FSMContext):
    text = message.text
    data = await state.get_data()
    user_id = data.get('user_id')

    await db.subtraction_user_balance(user_id=int(user_id), miqdor=int(text))
    await message.answer(text=f"<code>{user_id}</code> - dagi foydalanuvchining balansidan <code>{text}</code> "
                              "so'm oldingiz✅")
    await state.finish()


# Foydalanuvchini bloklash uchun
@dp.callback_query_handler(text="bloklash", state='*')
async def pul_qoshish(call: types.CallbackQuery, state: FSMContext):
    user_id = call.message.text.split('\n')[2].split(': ')[1]

    await db.add_user_to_ban(user_id=int(user_id))
    await call.message.answer(text="Foydalanuvchi bloklandi✅")
    await state.finish()

@dp.callback_query_handler(text='deleteruser', state='*')
async def delete_user(call: types.CallbackQuery, state: FSMContext):
    user_id = call.message.text.split('\n')[2].split(': ')[1]
    await call.message.delete()
    await db.delete_user(user_id=int(user_id))
    await call.message.answer(text="User is deleted")
    await state.finish()