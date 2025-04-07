import pytest
import pytest_asyncio
from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message, Chat, User
from core._routers import cmd_start, process_name
from aiogram.fsm.context import FSMContext
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные из .env

@pytest_asyncio.fixture
async def test_dispatcher():
    """Фикстура для создания тестового диспетчера"""
    bot = Bot(token=os.getenv("TEST_TOKEN"), default=DefaultBotProperties(parse_mode="HTML"))
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.bot = bot  # Добавляем атрибут bot
    yield dp
    await storage.close()

@pytest.mark.asyncio
async def test_cmd_start(test_dispatcher):
    """Тест команды /start"""
    message = Message(
        message_id=1,
        from_user=User(id=12345, is_bot=False, first_name="Test User"),
        chat=Chat(id=12345, type="private"),
        date=datetime.now(),
        text="/start"
    )
    state = FSMContext(bot=test_dispatcher.bot, storage=test_dispatcher.storage)

    await cmd_start(message, state)
    # Проверяем, что состояние FSM установлено
    assert await state.get_state() == "UserData:name"

@pytest.mark.asyncio
async def test_process_name(test_dispatcher):
    """Тест обработки имени"""
    message = Message(
        message_id=1,
        from_user=User(id=12345, is_bot=False, first_name="Test User"),
        chat=Chat(id=12345, type="private"),
        date=datetime.now(),
        text="Иван"
    )
    state = FSMContext(bot=test_dispatcher.bot, storage=test_dispatcher.storage)
    await state.set_state("UserData:name")

    await process_name(message, state)
    # Проверяем, что состояние FSM изменилось
    assert await state.get_state() == "UserData:date"
    # Проверяем сохраненные данные
    data = await state.get_data()
    assert data["name"] == "Иван"