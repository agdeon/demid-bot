import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.storage import StateMemoryStorage

import os
from dotenv import load_dotenv

from src.handlers.command_handler import *
from src.handlers.command_handler import CommandHandler
from src.handlers.callback_query_handler import CallbackQueryHandler
from src.handlers.text_handler import TextHandler


load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
storage = StateMemoryStorage()
bot = telebot.TeleBot(BOT_TOKEN, state_storage=storage)

command_handler = CommandHandler(bot)
text_handler = TextHandler(bot)
callback_query_handler = CallbackQueryHandler(bot)

# Запуск бота
if __name__ == "__main__":
    print("Бот запущен")
    bot.infinity_polling()