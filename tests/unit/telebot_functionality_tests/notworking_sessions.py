import os

import telebot
from dotenv import load_dotenv
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage

load_dotenv()

storage = StateMemoryStorage()
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN, state_storage=storage)

# Определение состояний
class UserStates(StatesGroup):
    waiting_for_name = State()  # Ожидание имени
    waiting_for_age = State()   # Ожидание возраста

# Команда /start: Начало сессии
@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.set_state(message.from_user.id, UserStates.waiting_for_name, message.chat.id)
    bot.send_message(message.chat.id, "Привет! Как тебя зовут?")

# Обработчик для ввода имени
@bot.message_handler(state=UserStates.waiting_for_name)
def name_handler(message):
    print(f"name_handler start")
    name = message.text  # Сохраняем имя
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = name  # Сохраняем имя в данных сессии
    bot.set_state(message.from_user.id, UserStates.waiting_for_age, message.chat.id)
    bot.send_message(message.chat.id, f"Приятно познакомиться, {name}! Сколько тебе лет?")

# Обработчик для ввода возраста
@bot.message_handler(state=UserStates.waiting_for_age)
def age_handler(message):
    age = message.text  # Сохраняем возраст
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        name = data.get('name', 'Неизвестно')
        data['age'] = age  # Сохраняем возраст в данных сессии
    bot.send_message(message.chat.id, f"Спасибо, {name}! Я запомнил, что тебе {age} лет.")
    bot.delete_state(message.from_user.id, message.chat.id)  # Сбрасываем состояние

# Команда /reset: Сброс сессии
@bot.message_handler(commands=['reset'])
def reset_handler(message):
    bot.delete_state(message.from_user.id, message.chat.id)
    bot.send_message(message.chat.id, "Твоя сессия сброшена. Напиши /start, чтобы начать заново.")

# Запуск бота
bot.polling(none_stop=True)