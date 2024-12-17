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
    bot.delete_message(message.chat.id, user_message_id)
    sent_message = bot.send_message(message.chat.id, "Привет!")
    time.sleep(3)
    bot.edit_message_text("Приветственное было сообщение отредактировано.", message.chat.id, sent_message.message_id)


bot.infinity_polling()