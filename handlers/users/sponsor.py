from loader import dp, db, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from data.config import ADMINS
from states.admin import AddSponsor
from keyboards.inline.panel import add_sponsor, sponsor_add


@dp.message_handler(text="📢 Majburiy obuna", state='*', user_id=ADMINS[0])
async def sponsor_channel(message: types.Message, state: FSMContext):
    panel = await db.select_row_panel()
    result = "<b>Majburiy obuna kanallar ro'yhati📃</b>\n\n"
    try:
        for item in panel:
            result += f"{item[1]}\n"
        await bot.send_message(chat_id=ADMINS[0], text=result,
                       reply_markup=add_sponsor)
    except Exception as error:
        print(error)
        await bot.send_message(chat_id=ADMINS[0], text=f"Majburiy obuna uchun kanal yo'q", reply_markup=add_sponsor)

# For add sponsor channel
@dp.callback_query_handler(text="addsponsor", state='*')
async def add_sponsor_channel(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    panel = await db.select_row_panel()
    if len(panel) < 6:
        await bot.send_message(chat_id=call.message.chat.id, text="Kanal qo'shish uchun kanal linkini yuboring\n"
                                      "Bot majburiy obuna ulamoqchi bo'lgan kanalingizda admin bo'lishi shart❗️\n\n"
                                      "<b>Exm: @blogca</b>")
        await AddSponsor.username.set()
    else:
        await bot.send_message(chat_id=call.message.chat.id,
                               text="<b>Siz eng ko'pi bilan 6 ta kanal qo'sha olasiz👮</b>")
        await state.finish()

@dp.message_handler(state=AddSponsor.username)
async def state_first_sponsor(message: types.Message, state: FSMContext):
    username = message.text
    try:
        if '@' in username:
            await db.add_channel(channel=username)
            await message.answer(text="Kanal bazaga qo'shildi✅", reply_markup=sponsor_add)
            await state.finish()
        else:
            await bot.send_message(chat_id=message.chat.id, text="Iltimos, kanal linki oldidan `@` qo'yishni "
                                                                 "unutmang!\n\nBoshqatta link yuboring👇")
            await AddSponsor.username.set()
    except:
        await message.answer(text="Kechirasiz, siz bu kanalni avval qo'shgan ekansiz iltimos boshqa kanal qo'shishga harak qilib ko'ring!", reply_markup=add_sponsor)
        await AddSponsor.username.set()

