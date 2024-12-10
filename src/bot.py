import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

from dotenv import load_dotenv

from handlers.command_handler import CommandHandler
from handlers.message_handler import MessageHandler
from handlers.callback_query_handler import CallbackQueryHandler

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

command_handler = CommandHandler(bot)
message_handler = MessageHandler(bot)
callback_query_handler = CallbackQueryHandler(bot)

command_handler.register_handlers()
message_handler.register_handlers()
callback_query_handler.register_handlers()

# Запуск бота
if __name__ == "__main__":
    print("Бот запущен")
    bot.infinity_polling()