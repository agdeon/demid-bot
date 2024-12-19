import logging
from pathlib import Path
from typing import Union

from src.utils.bot_data import BotData
from src.utils.misc_functions import read_json_from_file, write_json_to_file
from src.utils.static_classes import Languages, Ranks


class UserData:
    USERS_DATA_SUB_PATH = Path('botdata') / 'users_data'

    CONSOLE_LOG_LVL = logging.INFO
    FILE_LOG_LVL = logging.INFO

    def __init__(self, user_id):
        self.id = str(user_id)
        current_path = Path(__file__).resolve()
        self.users_folder_path = Path(current_path.parents[2]) / self.USERS_DATA_SUB_PATH
        self.user_folder_path = Path(self.users_folder_path) / self.id
        self.ensure_path_exists(self.user_folder_path)

        # Создание всех файлов данных юзера и привязка их к UserData для дальнейшего управления ими
        self.config = self.Config(self)
        self.gpt_history = self.GptHistory(self)
        self.gpt_presets = self.GptPresets(self)
        self.stats = self.GptStats(self)
        self.logger = self.Logger(self)

    @staticmethod
    def ensure_path_exists(path: Union[Path, str]):
        dir_path = Path(path)
        dir_path.mkdir(parents=True, exist_ok=True)

    class Config:
        FILENAME = 'cfg.json'

        def __init__(self, userdata_instance):
            self.userdata_instance = userdata_instance
            self.path = Path(userdata_instance.user_folder_path) / self.FILENAME
            if not self.path.exists():
                self._initialize()

        def load(self) -> Union[dict, list]:
            return read_json_from_file(self.path)

        def write(self, json_data: Union[dict, list]):
            return write_json_to_file(self.path, json_data)

        def _initialize(self):
            default_json = {
                "id": self.userdata_instance.id,
                "language": Languages.RU,
                "rank": Ranks.BASIC,
                "is_admin": False,
                "is_blocked": False,
                "gpt_history_enabled": False,
                "gpt_active_preset": None
            }
            self.write(default_json)

    class GptHistory:
        FILENAME = 'gpt_history.json'
        DEFAULT_JSON = []

        def __init__(self, userdata_instance):
            self.userdata_instance = userdata_instance
            self.path = Path(userdata_instance.user_folder_path) / self.FILENAME
            if not self.path.exists():
                self._initialize()

        def load(self) -> Union[dict, list]:
            return read_json_from_file(self.path)

        def write(self, json_data: Union[dict, list]):
            return write_json_to_file(self.path, json_data)

        def _initialize(self):
            self.write(self.DEFAULT_JSON)

    class GptPresets:
        FILENAME = 'gpt_presets.json'
        DEFAULT_JSON = [
            {
                "name": "Обычный GPT4",
                "instruction": ""
            },
            {
                "name": "Лаконичный GPT4",
                "instruction": "Отвечай лаконично и по делу. Без воды и лишних слов."
            },
            {
                "name": "Карточки слов",
                "instruction": "Твоя задача получать английское слово, затем вывести это слово, его транскрипцию, 3 наиболее популярных перевода этого слова. Затем несколько примеров его употребления с переводами. Если ты получаешь что-то другое кроме английского слова или фразы, отвечай так: ОТКАЗАНО: ВХОДНЫЕ ДАННЫЕ НЕКОРРЕКТНЫ."
            },
        ]

        def __init__(self, userdata_instance):
            self.userdata_instance = userdata_instance
            self.path = Path(userdata_instance.user_folder_path) / self.FILENAME
            if not self.path.exists():
                self._initialize()

        def load(self) -> Union[dict, list]:
            return read_json_from_file(self.path)

        def write(self, json_data: Union[dict, list]):
            write_json_to_file(self.path, json_data)

        def _initialize(self):
            self.write(self.DEFAULT_JSON)

    class GptStats:
        FILENAME = 'gpt_stats.json'
        DEFAULT_JSON = {
            "total_requests": 0,
            "total_tokens_spent": 0,
            "total_cost": 0,
            "today_requests": 0,
            "today_tokens_spent": 0,
            "today_cost": 0,
            "last_request_date": None
        }

        def __init__(self, userdata_instance):
            self.userdata_instance = userdata_instance
            self.path = Path(userdata_instance.user_folder_path) / self.FILENAME
            if not self.path.exists():
                self._initialize()

        def load(self) -> Union[dict, list]:
            return read_json_from_file(self.path)

        def write(self, json_data: Union[dict, list]):
            return write_json_to_file(self.path, json_data)

        def _initialize(self):
            self.write(self.DEFAULT_JSON)

    class Logger:
        FILENAME = 'user_log.log'

        def __init__(self, userdata_instance):
            self.userdata_instance = userdata_instance
            self.path = Path(userdata_instance.user_folder_path) / self.FILENAME
            if not self.path.exists():
                self._initialize()

            self._logger = logging.getLogger('USER_' + self.userdata_instance.id)
            self.bind_handlers()

        def debug(self, text):
            self._logger.debug(text)

        def info(self, text):
            self._logger.info(text)

        def error(self, text):
            self._logger.error(text)

        def bind_handlers(self):
            self._logger.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

            console_handler = logging.StreamHandler()
            console_handler.setLevel(self.userdata_instance.CONSOLE_LOG_LVL)
            console_handler.setFormatter(formatter)

            file_handler = logging.FileHandler(self.path, encoding='utf-8')
            file_handler.setLevel(self.userdata_instance.FILE_LOG_LVL)
            file_handler.setFormatter(formatter)

            self._logger.addHandler(console_handler)
            self._logger.addHandler(file_handler)

        def unbind_handlers(self):
            logger = self._logger
            for handler in logger.handlers[:]:  # Итерируем по копии списка, чтобы безопасно удалять
                if isinstance(handler, logging.FileHandler):
                    logger.removeHandler(handler)
                    handler.close()

        def _initialize(self):
            with open(self.path, 'w', encoding='utf-8') as file:
                pass  # пустой


if __name__ == '__main__':
    user_data = UserData('5155411')


