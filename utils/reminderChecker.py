import sqlite3, asyncio
from datetime import date

# TODO: Переписать под новый db.models

async def check_reminders():
    while True:
        today = date.today()
        
        cursor.execute('SELECT telegram_id, message FROM "birthday_remind" WHERE remind_date = ?', (today,))
        reminders = cursor.fetchall()

        for reminder in reminders:
            telegram_id, message = reminder
            await bot.send_message(telegram_id, f"Напоминание: {message}")

        # Удаляем отправленные напоминания (или обновляем remind_date на следующий год)
        cursor.execute('DELETE FROM "birthday_remind" WHERE remind_date = ?', (today,))
        conn.commit()

        # Проверяем напоминания каждые 60 секунд
        await asyncio.sleep(600)