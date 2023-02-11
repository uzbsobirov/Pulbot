from loader import db, dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.message_handler(text="To'lovlar tarixi 🧾", state='*')
async def pay_history(message: types.Message, state: FSMContext):
    panel = await db.select_from_panel(id=1)
    args = panel[0][1].split(', ')
    channel = args[0]
    group = args[1]
    # We must get channel and group invite link like this -> 'https://t.me/...'
    if channel.startswith('https://t.me/') and group.startswith('https://t.me/'):
        # Create Inline button for channel and group
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(text="Kanalga kirish 🧾", url=f'{channel}'))
        markup.add(types.InlineKeyboardButton(text="Izohlar 📝", url=f'{group}'))

        text = "<b>Botimiz haqiqatdan ham to'lab beradi. ✅</b>\n\n"
        text += f"<i>Quyidagi kanal orqali to'lovlar tarixini kuzatib borishingiz mumkin👇\n{channel}</i>"
        await message.reply(text=text, reply_markup=markup, disable_web_page_preview=True)
    else:

        chat_channel = await bot.get_chat(channel)
        channel_link = await chat_channel.export_invite_link()
        group_channel = await bot.get_chat(group)
        group_link = await group_channel.export_invite_link()

        # Create Inline button for channel and group
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(text="Kanalga kirish 🧾", url=f'{channel_link}'))
        markup.add(types.InlineKeyboardButton(text="Izohlar 📝", url=f'{group_link}'))

        text = "<b>Botimiz haqiqatdan ham to'lab beradi. ✅</b>\n\n"
        text += f"<i>Quyidagi kanal orqali to'lovlar tarixini kuzatib borishingiz mumkin👇\n{channel_link}</i>"
        await message.reply(text=text, reply_markup=markup, disable_web_page_preview=True)
