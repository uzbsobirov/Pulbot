from aiogram.dispatcher.filters.state import State, StatesGroup

class Reklama(StatesGroup):
    text = State()
    image = State()
    image_text = State()
    video = State()
    video_text = State()
    mediagroup = State()
