import telebot
import openai
from dotenv import load_dotenv
import os


load_dotenv()
# Токены
OPENAI_API_KEY = os.getenv('GPT_TOKEN')  # Вставь свой API-ключ от OpenAI
TELEGRAM_API_TOKEN = os.getenv('BOT_TOKEN')
# Инициализация бота и OpenAI
bot = telebot.TeleBot(TELEGRAM_API_TOKEN)
openai.api_key = OPENAI_API_KEY


# Функция для общения с GPT-4 (или другой моделью)
def ask_gpt(prompt):
    try:
        # Запрос к GPT-4 с использованием метода ChatCompletion.create
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Используем модель GPT-4 или другую модель по вашему выбору
            messages=[{"role": "user", "content": prompt}],  # Передаем запрос пользователя
            max_tokens=150,  # Ограничение на количество токенов в ответе
            temperature=0.7  # Температура модели, определяет креативность ответа
        )
        return response['choices'][0]['message']['content'].strip()  # Возвращаем ответ от модели
    except Exception as e:
        return f"Ошибка: {e}"

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Привет! Я бот с доступом к GPT-4. Напишите мне что угодно, и я постараюсь ответить!"
    )

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text  # Получаем текст пользователя
    bot.send_message(message.chat.id, "Думаю над ответом...")

    # Запрос к GPT-4 для получения ответа
    gpt_response = ask_gpt(user_input)

    # Отправляем ответ от GPT-4 пользователю
    bot.send_message(message.chat.id, gpt_response)

# Запуск бота
bot.polling()