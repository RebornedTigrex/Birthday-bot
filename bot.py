import asyncio
import logging
from utils.bot_instance import bot, dp
from utils.reminder_service import ReminderChecker  # Импортируем ReminderChecker для проверки напоминаний

# Настройка логгера
logger = logging.getLogger(__name__)

# Логирование остановки бота
async def bot_stopped():
    logger.critical("Bot has been stopped")

# Основная функция запуска бота
async def main():
    # Создаем объект для проверки напоминаний
    reminder_checker = ReminderChecker(bot=bot, check_interval=600)  # Передаем объект бота

    # Регистрируем обработчик остановки бота
    dp.shutdown.register(bot_stopped)

    logger.info("Bot is starting...")

    # Запускаем задачи
    await asyncio.gather(
        dp.start_polling(bot),  # Запуск бота
        reminder_checker.start()  # Запуск проверки напоминаний
    )

# Запуск бота
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot has been stopped manually")

