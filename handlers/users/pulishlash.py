from loader import db, dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

# Handler for `Pul ishlash 💸`
@dp.message_handler(text="Pul ishlash 💸", state='*')
async def pulishlash(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username
    full_name = message.from_user.full_name
    mention = message.from_user.get_mention(f"{full_name}", as_html=True)
    
    # Agar foydalanuvchi `Ban` bazasida bo'lsa
    try:
        user = await db.select_one_ban_user(user_id=user_id)
        id = user[0][0]
        await message.answer(text="<b>Siz botdan bloklangansiz</b>", reply_markup=ReplyKeyboardRemove())
        await state.finish()
    except IndexError:
        catch = await db.select_one_users(user_id=user_id)
        deep_link = catch[0][6]
        photo = "https://t.me/forchrabot/52"
        await message.reply(text="<b>Quyidagi havolani doʻstlaringizga tarqatib pul ishlang! 👇</b>")
        if username:
            caption = f"✅ PuldorkuBot da har bir taklif qilgan do'stingiz uchun mukofot oling 🤖\n\n🎈 @{username} do'stingizdan unikal havola-taklifnoma.\n\n👇 Boshlash uchun bosing:\n{deep_link}"
            await message.answer_photo(photo=photo, caption=caption)
            await state.finish()
        else:
            caption = f"✅ PuldorkuBot da har bir taklif qilgan do'stingiz uchun mukofot oling 🤖\n\n🎈 {mention} do'stingizdan unikal havola-taklifnoma.\n\n👇 Boshlash uchun bosing:\n{deep_link}"
            await message.answer_photo(photo=photo, caption=caption)
            await state.finish()