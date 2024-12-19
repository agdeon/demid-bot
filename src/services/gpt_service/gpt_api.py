import openai
from dotenv import load_dotenv
import os


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

        try:
            load_dotenv()
            openai.api_key = os.getenv('GPT_TOKEN')
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=messages
            )
            return response['choices'][0]['message']['content'].strip()

        except Exception as e:
            return f"❗ ERROR: {e}"