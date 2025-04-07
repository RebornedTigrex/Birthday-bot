import pytest
from utils.reminder_service import ReminderChecker
from unittest.mock import AsyncMock
import asyncio
from datetime import date

@pytest.mark.asyncio
async def test_check_reminders(monkeypatch):
    """Тест проверки напоминаний"""
    mock_bot = AsyncMock()
    monkeypatch.setattr("bot.bot", mock_bot)

    # Передаем mock_bot в ReminderChecker
    reminder_checker = ReminderChecker(bot=mock_bot, check_interval=1)

    # Мокируем метод query и filter_by
    mock_query = AsyncMock()
    mock_query.filter_by.return_value = [
        type("BirthdayRemind", (object,), {"telegram_id": "12345", "message": "Напоминание", "remind_date": date.today()})()
    ]
    monkeypatch.setattr(reminder_checker.session, "query", lambda *args: mock_query)

    # Запускаем проверку напоминаний в отдельной задаче
    task = asyncio.create_task(reminder_checker.check_reminders())

    # Ждем немного, чтобы цикл выполнился
    await asyncio.sleep(2)

    # Останавливаем цикл
    await reminder_checker.stop()
    await task  # Дожидаемся завершения задачи

    # Проверяем, что сообщение было отправлено
    mock_bot.send_message.assert_called_once_with("12345", "Напоминание")