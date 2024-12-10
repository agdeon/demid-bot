import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = types.KeyboardButton("Test Button 1")
    b2 = types.KeyboardButton("Test Inline Buttons")
    markup.add(b1, b2)
    bot.send_message(message.chat.id, "Choose button", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Test Button 1")
def handle_message(message):
    bot.send_message(message.chat.id, f"You chose: \"{message.text}\"!")


@bot.message_handler(func=lambda message: message.text == "Test Inline Buttons")
def handle_message(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Inline Button 1", callback_data="button_1"))
    markup.add(InlineKeyboardButton("Inline Button 2", callback_data="button_2"))
    bot.send_message(message.chat.id, "Choose button:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "button_1":
        bot.answer_callback_query(call.id, "Вы нажали Inline Кнопку 1!")
        bot.send_message(call.message.chat.id, "Вы выбрали Inline Кнопку 1.")
    elif call.data == "button_2":
        bot.answer_callback_query(call.id, "Вы нажали Inline Кнопку 2!")
        bot.send_message(call.message.chat.id, "Вы выбрали Inline Кнопку 2.")


bot.polling(none_stop=True)