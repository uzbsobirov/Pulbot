from aiogram.dispatcher.filters.state import State, StatesGroup

class Control(StatesGroup):
    control = State()
    add = State()
    subtraction = State()