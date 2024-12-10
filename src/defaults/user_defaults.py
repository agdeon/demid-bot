from pathlib import Path
from ranks import UserRanks
from languages import Languages

class UserDefaults:
    """
    Класс определяет данные пользователя по умолчанию
    """
    GPT_HISTORY_ENABLED = False
    RANK = UserRanks.BASIC
    LANGUAGE = Languages.RU

    LOG_FILENAME = 'user.log'
    GPT_HISTORY_FILENAME = 'gpt_history.json'
    CFG_FILENAME = 'user.cfg'
    STAT_FILENAME = 'gpt_request_stats.json'
    GPT_PRESETS_FILENAME = 'gpt_presets.json'

    PRESETS = [
        {
            "name": "Обычный GPT4",
            "preset": ""
        },
        {
            "name": "Лаконичный GPT4",
            "preset": "Отвечай лаконично и по делу. Без воды и лишних слов."
        },
        {
            "name": "Карточки слов",
            "preset": "Твоя задача получать английское слово. Затем вывести это слово, его транскрипцию, 3 наиболее популярных перевода этого слова. Затем несколько примеров его употребления с переводами. Если ты получаешь что-то другое кроме английского слова или фразы, отвечай так: ОТКАЗАНО: ВХОДНЫЕ ДАННЫЕ НЕКОРРЕКТНЫ."
         },
    ]