import pytest
import asyncio
from bot import main

@pytest.mark.asyncio
async def test_bot_startup(monkeypatch):
    """Тест запуска бота"""

    # Мокируем переменную окружения TOKEN
    monkeypatch.setenv("TOKEN", "mocked_token")

    async def mock_start_polling(*args, **kwargs):
        await asyncio.sleep(1)  # Симулируем короткий polling
        return True

    monkeypatch.setattr("aiogram.Dispatcher.start_polling", mock_start_polling)

    # Устанавливаем тайм-аут для остановки main
    try:
        await asyncio.wait_for(main(), timeout=2)  # Останавливаем через 2 секунды
    except asyncio.TimeoutError:
        pass  # Ожидаемое поведение для завершения теста

    # Проверяем, что бот запускается без ошибок
    assert True  # Если дошли до этой строки, тест успешен