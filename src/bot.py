import os

import telebot
from dotenv import load_dotenv

from src.handlers.callback_query_handler import CallbackQueryHandler
from src.handlers.command_handler import CommandHandler
from src.handlers.text_handler import TextHandler

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

command_handler = CommandHandler(bot)
text_handler = TextHandler(bot)
# callback_query_handler = CallbackQueryHandler(bot)

command_handler.register_handlers()
text_handler.register_handlers()

# Запуск бота
if __name__ == "__main__":
    print("DemidBot is running")
    bot.infinity_polling()