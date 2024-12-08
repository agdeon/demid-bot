import telebot
from telebot import types
import os

from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = types.KeyboardButton("Тестовая кнопка 1")
    b2 = types.KeyboardButton("Тестовая кнопка 2")
    markup.add(b1, b2)
    bot.send_message(message.chat.id, "TESTMSG: Вы ввели команду /start!", reply_markup=markup)

# Обработчик нажатия на кнопку
@bot.message_handler(func=lambda message: True)
def handle_message(message):

    bot.send_message(message.chat.id, f"TESTMSG: Вы нажали на кнопку \"{message.text}\"!")


# Запуск бота
bot.polling(none_stop=True)