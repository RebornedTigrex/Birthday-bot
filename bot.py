import sqlite3, logging, asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from utils import (configActions as config, custom_logger as cl)

TOKEN = config.takeParam("TOKEN")

redis = Redis(host='localhost', port=6379, db=0)
storage = RedisStorage(redis)

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='html'))
dp = Dispatcher(storage=storage)

async def bot_stopped():
    cl.log("Bot", "critical", f"Bot has been stopped")

async def main():
    tasks = [
        dp.start_polling(bot)
    ]
    dp.shutdown.register(bot_stopped)
    await asyncio.gather(*tasks)

    