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

# For `Minimal summa`
class MinSum(StatesGroup):
    summa = State()


# For `Taklif summa`
class TaklifSumma(StatesGroup):
    summa = State()

# For `Xabar yuborish`
class SendMessage(StatesGroup):
    message = State()

# <----------Majburiy obuna---------->
class AddSponsor(StatesGroup):
    first = State()
    second = State()
    third = State()
    fourth = State()
    fifth = State()
    sixth = State()

