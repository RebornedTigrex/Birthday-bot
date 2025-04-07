import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
from dotenv import load_dotenv, find_dotenv

# Настройка логгера
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Загрузка переменных из .env только если они не заданы
if not os.getenv("TOKEN"):
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())

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