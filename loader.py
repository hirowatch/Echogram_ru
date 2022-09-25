import logging
import asyncio
from aiogram.bot import Bot
from aiogram.types import ParseMode
from aiogram.dispatcher import Dispatcher
from configparser import ConfigParser
from aiogram.contrib.fsm_storage.memory import MemoryStorage

config = ConfigParser()
storage = MemoryStorage()
config.read("data/config.ini")
loop = asyncio.get_event_loop()

bot = Bot(token=config["aiogram"]["bot_token"], parse_mode=ParseMode.HTML)
dp = Dispatcher(bot=bot, loop=loop, storage=storage)

logging.basicConfig(filename="logs.log", level=logging.INFO)
