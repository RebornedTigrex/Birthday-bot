from aiogram.fsm.state import State, StatesGroup

async def tryFinish(state):
    try:
        await state.clear()
    except:
        pass

class UserData(StatesGroup):
    name = State() 
    date = State()
    message_remind = State()

# class State(StatesGroup):
#     State = State()

# class ContactWithDevs(StatesGroup):
#     Message = State()