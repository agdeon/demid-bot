import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv('GPT_TOKEN')

# WORKING EXAMPLE

def ask_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Указываем модель GPT-4
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        # Возвращаем ответ
        return response['choices'][0]['message']['content'].strip()

    except Exception as e:
        return f"Ошибка: {e}"

prompt = "Привет?"
response = ask_gpt(prompt)
print(response)

