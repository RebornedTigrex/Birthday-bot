from aiogram.fsm.state import State, StatesGroup

class UserData(StatesGroup):
    waiting_for_birthday = State() 
    