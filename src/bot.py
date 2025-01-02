import os
import time
import sys

import telebot
from dotenv import load_dotenv

src_abs_path = os.path.abspath("")  # Преобразуем относительный путь root папки в абсолютный
print(src_abs_path)
sys.path.append(src_abs_path)  # Добавляем для поиска модулей

from handlers.callback_query_handler import CallbackQueryHandler
from handlers.command_handler import CommandHandler
from handlers.text_handler import TextHandler

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
    try:
        print("DemidBot is running")
        bot.infinity_polling()
    except Exception as e:
        print(e)
        time.sleep(20)
