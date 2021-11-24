import asyncio
from data import config, db
from aiogram import Bot, Dispatcher

loop = asyncio.get_event_loop()
bot = Bot(token=config.TOKEN, parse_mode="HTML")
dp = Dispatcher(bot=bot, loop=loop)
