import openai
from dotenv import load_dotenv
import os
import time

class GPTApiService:

    @staticmethod
    def request(string_or_messages: list | str):
        """
        Sends request to GPT
        Messages format:
            For gpt history tracking {"role": "assistant", "content": "gpt response"}
            For user requests {"role": "user", "content": "some user requests"}
            For gpt instructions {"role": "system", "content": "Your instruction for gpt"}

        :param string_or_messages: Should be list [] of objects -> {"role": "user", "content": prompt}, or string
        :type string_or_messages: str or list
        :return: Returns string
        """

        if isinstance(string_or_messages, str):
            messages = [{"role": "user", "content": string_or_messages}]
        else:
            messages = string_or_messages

        try_cnt = 0
        result = None

        while try_cnt < 5:
            try_cnt = try_cnt + 1

            try:
                load_dotenv()
                openai.api_key = os.getenv('GPT_TOKEN')
                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=messages
                )
                result = response['choices'][0]['message']['content'].strip()
                break  # Получен результат, выходим с цикла
            except Exception as e:
                result = f"❗ ERROR: {e}"
            time.sleep(0.3)

        return result