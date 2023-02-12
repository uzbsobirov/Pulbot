from loader import dp, db, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from data.config import ADMINS
from states.admin import AddSponsor
from keyboards.inline.panel import add_sponsor


@dp.message_handler(text="📢 Majburiy obuna", state='*', user_id=ADMINS[0])
async def sponsor_channel(message: types.Message, state: FSMContext):
    panel = await db.select_row_panel()
    if panel[0][1]:
        await bot.send_message(chat_id=ADMINS[0], text=f"Majburiy obuna kanallar ro'yhati\n\n{panel[0][6]}",
                               reply_markup=add_sponsor)
    else:
        await bot.send_message(chat_id=ADMINS[0], text=f"Majburiy obuna uchun kanal yo'q", reply_markup=add_sponsor)

# For add sponsor channel
@dp.callback_query_handler(text="addsponsor", state='*')
async def add_sponsor_channel(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await bot.send_message(chat_id=ADMINS[0], text="Kanal qo'shish uchun kanal linkini yuboring\n\n<b>Exm: @blogca</b>")
    await AddSponsor.first.set()

@dp.message_handler(state=AddSponsor.first)
async def state_first_sponsor(message: types.Message, state: FSMContext):
    first_sponsor = message.text
    print(first_sponsor)
    await state.finish()

