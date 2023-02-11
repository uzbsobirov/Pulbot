from loader import db, dp
from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.message_handler(text="Top 📊", state='*')
async def user_top(message: types.Message, state: FSMContext):
    top_users = await db.select_all_users()
    result = "Top eng ko'p referal yig'gan foydalanuvchilar👇\n\n"
    number = 1
    lst = []
    # Tsikl aylantiramiz
    for top_user in top_users:
        # Get user datas
        full_name = top_user[1] # Full name
        user = message.from_user.get_mention(f"{full_name}", as_html=True) # Get mention / direct
        count = top_user[8] # Referal count
        lst.append(str(count))
        result += f"{number}) {user} -- {count}\n"
        number += 1
    # sort = sorted(lst, reverse=True)
    # print(sort)
    await message.answer(text=result)
    await state.finish()