import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
from dotenv import load_dotenv
import os

from utils.reminder_service import ReminderChecker  # Импортируем ReminderChecker для проверки напоминаний

# Настройка логгера
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Загрузка переменных из .env
load_dotenv()

# Получение параметров из переменных окружения
TOKEN = os.getenv("TOKEN")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost:6379")

# Проверка наличия обязательных переменных
if not TOKEN:
    logger.critical("Переменная окружения TOKEN не задана")
    raise ValueError("Переменная окружения TOKEN не задана")

# Настройка Redis для хранения состояний
redis_host, redis_port = REDIS_HOST.split(":")
redis = Redis(host=redis_host, port=int(redis_port), db=0)
storage = RedisStorage(redis)

# Создание объекта бота и диспетчера
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='html'))
dp = Dispatcher(storage=storage)

# Логирование остановки бота
async def bot_stopped():
    logger.critical("Bot has been stopped")

# Основная функция запуска бота
async def main():
    # Создаем объект для проверки напоминаний
    reminder_checker = ReminderChecker(check_interval=600)  # Интервал проверки 10 минут

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

