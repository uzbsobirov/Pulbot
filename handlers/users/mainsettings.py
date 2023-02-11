from loader import dp, db, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from data.config import ADMINS
from keyboards.inline.panel import mainsettings

@dp.message_handler(text="⚙️ Asosiy sozlamalar", state='*', user_id=ADMINS[0])
async def main_settings(message: types.Message, state: FSMContext):
    await message.answer(text="<b>️ Asosiy sozlamalar</b> bo'limiga xush kelibsiz", reply_markup=mainsettings)