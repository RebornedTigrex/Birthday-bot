import pytest
from utils.reminder_service import ReminderChecker
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_check_reminders(monkeypatch):
    """Тест проверки напоминаний"""
    mock_bot = AsyncMock()
    monkeypatch.setattr("bot.bot", mock_bot)

    reminder_checker = ReminderChecker(check_interval=1)
    reminder_checker.session.query = AsyncMock(return_value=[
        {"telegram_id": "12345", "message": "Напоминание"}
    ])

    await reminder_checker.check_reminders()
    mock_bot.send_message.assert_called_once_with("12345", "Напоминание")