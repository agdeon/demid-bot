from src.utils.user_data import UserData
from src.utils.bot_data import BotData
from src.services.gpt_service.gpt_api import GPTApiService
from src.services.gpt_service.gpt_response_formatter import  GPTResponseHTMLFormatter

class GPTManager:

    def __init__(self, user_id):
        self.user_id = str(user_id)
        self.userdata = UserData(self.user_id)
        self.botdata = BotData()
        self.messages = []

    def ask_gpt(self, question_text):
        """
        Sends request to GPT
        Messages format:
            For gpt history responses {"role": "assistant", "content": "gpt response"}
            For user requests {"role": "user", "content": "some user requests"}
            For gpt instructions {"role": "system", "content": "Your instruction for gpt"}
        """

        if self._is_history_empty():
            self._messages_add_system_entry(self._get_active_preset_content())
            self._messages_add_question_entry(question_text)
        else:
            self._messages_add_system_entry(self._get_active_preset_content())
            self.messages = self.messages + self.userdata.gpt_history.load()
            self._messages_add_question_entry(question_text)
        self._manage_messages_limit()

        response_text = GPTApiService.request(self.messages)

        if self._is_history_enabled():
            self._messages_add_response_entry(response_text)
            self._save_history_messages()

        print(self.messages)
        return GPTResponseHTMLFormatter.format(response_text)

    def _messages_add_question_entry(self, text):
        self.messages.append({"role": "user", "content": text})

    def _messages_add_response_entry(self, text):
        self.messages.append({"role": "assistant", "content": text})

    def _messages_add_system_entry(self, instruction_text):
        self.messages.append({"role": "system", "content": instruction_text})

    def _is_history_enabled(self):
        return bool(self.userdata.config.load()["gpt_history_enabled"])

    def _manage_messages_limit(self):
        user_rank = self.userdata.config.load()["rank"]
        limit = self.botdata.ranks_settings.load().get(user_rank).get("history_messages_limit")
        while len(self.messages) > 0 and len(self.messages) > limit + 1:  # +1 bc of system content
            self.messages.pop(1)

    def _is_history_empty(self):
        if len(self.userdata.gpt_history.load()) == 0:
            return True
        return False

    def _get_active_preset_content(self):
        active_preset_name = self.userdata.config.load()["gpt_active_preset"]
        for preset in self.userdata.gpt_presets.load():
            if preset.get("name") == active_preset_name:
                return preset.get("instruction")
        raise Exception(f"Невозможно найти активный пресет с названием {active_preset_name} в списке пресетов пользователя.")

    def _save_history_messages(self):
        msgs_without_system_content = self.messages[1:]
        self.userdata.gpt_history.write(msgs_without_system_content)

if __name__ == '__main__':
    rsp = GPTManager(470286929).ask_gpt("Привет")
    print(rsp)