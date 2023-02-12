from loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.default.main import main, main_admin
from data.config import ADMINS

@dp.message_handler(text="◀️ Orqaga", state='*')
async def back_main(message: types.Message, state: FSMContext):
    if message.from_user.id == int(ADMINS[0]):
        await message.answer("<b>Siz asosiy menyudasiz🕳</b>", reply_markup=main_admin)
        await state.finish()
    else:
        await message.answer("<b>Siz asosiy menyudasiz🕳</b>", reply_markup=main)
        await state.finish()