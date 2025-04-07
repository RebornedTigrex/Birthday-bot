import pytest
from aiogram.types import Message
from core._routers import cmd_start, process_name, process_birthday
from aiogram.fsm.context import FSMContext

@pytest.mark.asyncio
async def test_cmd_start(test_dispatcher):
    """Тест команды /start"""
    message = Message(message_id=1, from_user={"id": 12345}, chat={"id": 12345}, text="/start")
    state = FSMContext(storage=test_dispatcher.storage, user_id=12345, chat_id=12345)

    await cmd_start(message, state)
    # Проверяем, что состояние FSM установлено
    assert await state.get_state() == "UserData:name"

@pytest.mark.asyncio
async def test_process_name(test_dispatcher):
    """Тест обработки имени"""
    message = Message(message_id=1, from_user={"id": 12345}, chat={"id": 12345}, text="Иван")
    state = FSMContext(storage=test_dispatcher.storage, user_id=12345, chat_id=12345)
    await state.set_state("UserData:name")

    await process_name(message, state)
    # Проверяем, что состояние FSM изменилось
    assert await state.get_state() == "UserData:date"
    # Проверяем сохраненные данные
    data = await state.get_data()
    assert data["name"] == "Иван"