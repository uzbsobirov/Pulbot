import aiogram
from loader import db, dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.message_handler(text="Qo'llanma 📄", state='*')
async def pay_history(message: types.Message, state: FSMContext):
    panel = await db.select_from_panel(id=1)
    try:
        manual = panel[0][2]
        admin = panel[0][3]
        # Create inline button for developer or admin profile
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(text="🖥 Dasturchi", url=f't.me/{admin}'))
        await message.reply(text=manual, reply_markup=markup)
        await state.finish()
    except:
        # Create inline button for developer or admin profile
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(text="🖥 Dasturchi", url='t.me/uzbsobirov'))
        await message.reply(text='This field is empty', reply_markup=markup)
        await state.finish()