import pytest
from bot import main

@pytest.mark.asyncio
async def test_bot_startup(monkeypatch):
    """Тест запуска бота"""
    async def mock_start_polling(*args, **kwargs):
        return True

    monkeypatch.setattr("aiogram.Dispatcher.start_polling", mock_start_polling)

    # Проверяем, что бот запускается без ошибок
    await main()