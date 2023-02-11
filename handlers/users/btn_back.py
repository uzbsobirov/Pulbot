from loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.default.main import main

@dp.message_handler(text="◀️ Orqaga", state='*')
async def back_main(message: types.Message, state: FSMContext):
    await message.answer("<b>Siz asosiy menyudasiz🕳</b>", reply_markup=main)
    await state.finish()