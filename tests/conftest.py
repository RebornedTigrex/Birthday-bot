import pytest_asyncio
import os
from dotenv import load_dotenv
from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

# Загружаем переменные из .env
load_dotenv()

@pytest_asyncio.fixture
async def test_dispatcher():
    """Фикстура для создания тестового диспетчера"""
    bot = Bot(token=os.getenv("TEST_TOKEN"), default=DefaultBotProperties(parse_mode='html'))
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    yield dp
    await storage.close()