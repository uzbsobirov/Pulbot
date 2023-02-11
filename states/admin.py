from aiogram.dispatcher.filters.state import State, StatesGroup

# For `Tolov tarixi`
class PayHistory(StatesGroup):
    channel = State()
    group = State()


# For `Qollanma`
class Manual(StatesGroup):
    text = State()

# For `Admin User`
class AdminUser(StatesGroup):
    username = State()