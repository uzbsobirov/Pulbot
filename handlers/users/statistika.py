import datetime
from loader import db, dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from data.config import ADMINS

# Handler for `📊 Statistika`
@dp.message_handler(text="📊 Statistika", state='*', user_id=ADMINS[0])
async def pulishlash(message: types.Message, state: FSMContext):
    users = await  db.count_users()
    today = datetime.date.today()
    text = f"<b>📆 Bugunki sana: {today}\n\n📊 Bot obunachilari: {users}\n\n⚡️@puldorkubot</b>"
    await message.reply(text=text)
    await state.finish()