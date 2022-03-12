from aiogram import Bot, Dispatcher
import sys, config
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage = MemoryStorage()

bot_token = config.BOT_TOKEN
if not bot_token:
    sys.exit('Нету токена')

bot = Bot(token=bot_token)
dp = Dispatcher(bot, storage=storage)