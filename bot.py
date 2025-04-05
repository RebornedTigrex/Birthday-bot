import sqlite3, logging, asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from utils import (configActions, custom_logger as cl)

config = configActions()

TOKEN = config.takeParam("TOKEN")
ip, port = config.takeParam("HOST").split(":")

redis = Redis(host=ip, port=port, db=0)
storage = RedisStorage(redis)

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='html'))
dp = Dispatcher(storage=storage)

async def bot_stopped():
    cl.log("Bot", "critical", f"Bot has been stopped")

async def main():
    tasks = [
        dp.start_polling(bot)
        
        #TODO: Метод проверки дат и отправки сообщений
        
    ]
    dp.shutdown.register(bot_stopped)
    await asyncio.gather(*tasks)

    