# bot.py

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters import Command
from aiogram.utils import executor
from config import API_TOKEN
from database import Database

# Import handlers and admin panel
import handlers
import admin

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Initialize database
db = Database()



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)