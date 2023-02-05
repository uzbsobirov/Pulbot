from aiogram.dispatcher.filters.state import State, StatesGroup

class Starting(StatesGroup):
    phone = State()