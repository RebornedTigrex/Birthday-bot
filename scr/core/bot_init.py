from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from tinydb import TinyDB, Query

from core.utils import configActions as config 

redis = Redis(host='localhost', port=6379, db=0)
storage = RedisStorage(redis)

db = TinyDB('birthdays.json')  # Файл для хранения данных
User = Query()

TOKEN = config._loadCfg()

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=storage)