import os

import telebot
from dotenv import load_dotenv

load_dotenv()


BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# Шаг 1: Спрашиваем имя
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Как тебя зовут?")
    bot.register_next_step_handler(message, process_name)

# Шаг 2: Обрабатываем имя и спрашиваем возраст
def process_name(message):
    name = message.text
    bot.send_message(message.chat.id, f"Приятно познакомиться, {name}! Сколько тебе лет?")
    bot.register_next_step_handler(message, process_age, name)

# Шаг 3: Обрабатываем возраст и выводим итог
def process_age(message, name):
    try:
        age = int(message.text)
        bot.send_message(message.chat.id, f"Спасибо, {name}! Ты сказал, что тебе {age} лет.")
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введи число для возраста.")
        bot.register_next_step_handler(message, process_age, name)

# Запуск бота
bot.polling(none_stop=True)