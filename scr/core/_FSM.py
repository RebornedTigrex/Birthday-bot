from aiogram.fsm.state import State, StatesGroup

class setBirthday(StatesGroup):
    custom_message_q = State()
    save_date_q = State()
    remind_q = State()
    
class takeBirthday(StatesGroup):
    list_all_dates = State()
    pop_or_close = State()
    
class goAhead(StatesGroup):
    raise NotImplementedError("Пока ничего нет.")
    