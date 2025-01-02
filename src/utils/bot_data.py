from pathlib import Path
from src.utils.misc_functions import read_json_from_file, write_json_to_file, create_empty_file_by_path

class BotData:

    # CFG_DEFAULT_DICT = {
    #     "white_list_enabled": True,
    #     "white_list": [2124452396, 470286929],
    #     "black_list": [],
    #     "ranks":

    # }

    ACTIVE_STATUS_STR = '✅ '
    ERROR_STATUS_STR = '⚠️ '
    BOTDATA_SUB_PATH = Path('botdata')

    def __init__(self):
        current_path = Path(__file__).resolve()
        self.folder_path = Path(current_path.parents[2]) / self.BOTDATA_SUB_PATH
        self._ensure_path_exists(self.folder_path)

        self.ranks_settings = self.RankSettings(self)
        self.whitelist = self.WhiteList(self)
        self.blacklist = self.BlackList(self)

    @staticmethod
    def _ensure_path_exists(path: Path):
        dir_path = Path(path)
        dir_path.mkdir(parents=True, exist_ok=True)

    class RankSettings:
        FILENAME = 'ranks.json'
        DEFAULT = {
            "basic": {
                "daily_tokens_limit": 4000,
                "history_tokens_limit": 500,
                "history_messages_limit": 5
            },
            "plus": {
                "daily_tokens_limit": 20000,
                "history_tokens_limit": 500,
                "history_messages_limit": 5
            },
            "vip": {
                "daily_tokens_limit": 40000,
                "history_tokens_limit": 1000,
                "history_messages_limit": 10
            },
            "admin": {
                "daily_tokens_limit": 40000,
                "history_tokens_limit": 1000,
                "history_messages_limit": 10
            }
        }

        def __init__(self, botdata_instance):
            self.path = Path(botdata_instance.folder_path) / self.FILENAME
            if not self.path.exists():
                self._initialize()

        def load(self):
            return read_json_from_file(self.path)

        def _initialize(self):
            write_json_to_file(self.path, self.DEFAULT)

    class WhiteList:
        FILENAME = 'whitelist.txt'

        def __init__(self, botdata_instance):
            self.path = Path(botdata_instance.folder_path) / self.FILENAME
            if not self.path.exists():
                self._initialize()

        def add(self, user_id):
            pass

        def remove(self, user_id):
            pass

        def _initialize(self):
            create_empty_file_by_path(self.path)

    class BlackList:
        FILENAME = 'blacklist.txt'

        def __init__(self, botdata_instance):
            self.path = Path(botdata_instance.folder_path) / self.FILENAME
            if not self.path.exists():
                self._initialize()

        def add(self, user_id):
            pass

        def remove(self, user_id):
            pass

        def _initialize(self):
            create_empty_file_by_path(self.path)


if __name__ == '__main__':
    BotData()