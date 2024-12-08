import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Кнопка 1", callback_data="button_1"))
    markup.add(InlineKeyboardButton("Кнопка 2", callback_data="button_2"))
    bot.send_message(message.chat.id, "Выберите кнопку:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "button_1":
        bot.answer_callback_query(call.id, "Вы нажали Кнопку 1!")
        bot.send_message(call.message.chat.id, "Вы выбрали Кнопку 1.")
    elif call.data == "button_2":
        bot.answer_callback_query(call.id, "Вы нажали Кнопку 2!")
        bot.send_message(call.message.chat.id, "Вы выбрали Кнопку 2.")


# Запуск бота
bot.infinity_polling()