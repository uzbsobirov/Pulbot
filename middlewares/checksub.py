import logging
from loader import dp, db, bot
from utils.misc.subscription import check
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
from data.config import CHANNELS

class BigBrother(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        if update.message:
            user = update.message.from_user.id
            if update.message.text in ['/start', '/help']:
                return
        elif update.callback_query:
            user = update.callback_query.from_user.id
            if update.callback_query.data in ['check_subs']:
                return
        else:
            return
        logging.info(user)
        result = str()
        markup = types.InlineKeyboardMarkup(row_width=1)
        final_status = True
        for channel in CHANNELS:
            status = await check(user_id=user, channel=channel)
            final_status *= status
            channel = await bot.get_chat(channel)
            invite_link = await channel.export_invite_link()
            if not status:
                result += f"{invite_link} kanaliga obuna chiqdingiz"
            markup.insert(types.InlineKeyboardButton(text=channel.title, url=invite_link))

        if not final_status:
            await update.message.answer(result, disable_web_page_preview=True)
            raise CancelHandler()