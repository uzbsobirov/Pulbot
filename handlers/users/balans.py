from loader import db, dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

# Handler for `Balans 💰`
@dp.message_handler(text="Balans 💰", state='*')
async def pulishlash(message: types.Message, state: FSMContext):
    pass