import logging
from aiogram.fsm.state import State, StatesGroup

# Настройка логгера
logger = logging.getLogger(__name__)

async def tryFinish(state):
    """
    Попытка завершить текущее состояние FSM.
    :param state: FSMContext
    """
    try:
        await state.clear()
        logger.info("Состояние FSM успешно завершено.")
    except Exception as e:
        logger.error(f"Ошибка при завершении состояния FSM: {e}")

class UserData(StatesGroup):
    """
    Состояния для работы с данными пользователя.
    """
    name = State()  # Ввод имени
    date = State()  # Ввод даты рождения
    message_remind = State()  # Ввод сообщения для напоминания
    delete_name = State()  # Удаление напоминания
    logger.info("Состояния FSM для UserData инициализированы.")