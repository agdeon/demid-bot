import os
import time

import telebot
from dotenv import load_dotenv
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_message_id = message.message_id
    sent_message = bot.send_message(message.chat.id, "Это первое сообщение.")
    time.sleep(1)
    bot.delete_message(message.chat.id, sent_message.message_id)
    bot.delete_message(message.chat.id, user_message_id)
    sent_message = bot.send_message(message.chat.id, "Это новое сообщение!")
    time.sleep(1)
    bot.delete_message(message.chat.id, sent_message.message_id)


bot.infinity_polling()