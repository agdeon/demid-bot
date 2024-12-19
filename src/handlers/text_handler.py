from src.keyboards.reply_keyboards import ReplyKeyboards
from src.utils.bot_data import BotData
from src.utils.user_data import UserData
from src.services.gpt_service.gpt_manager import GPTManager

class TextHandler:

    def __init__(self, bot):
        self.bot = bot

    def _text_handler(self, message):
        userid = message.from_user.id
        # Если это текст из кнопок пресетов - обрабатываем нажатие на кнопку
        if self._check_if_preset_button(message.text, userid):
            self._button_handler(message)
            return
        # Если любая команда - игнорируем
        elif message.text[0] == '/':
            return
        # Обычный текст - запрос в гпт
        else:
            try:
                reply = GPTManager(userid).ask_gpt(message.text)
            except Exception as e:
                reply = BotData.ERROR_STATUS_STR + str(e)
            print(reply)
            self.bot.send_message(userid, reply, parse_mode='HTML')


    def _button_handler(self, message):
        preset_name = self._remove_active_status_str(message.text)
        user_id = message.from_user.id
        cfg = UserData(user_id).config.load()
        if cfg["gpt_active_preset"] == preset_name:
            self._show_preset_info(preset_name, user_id)
        else:
            self._make_active_preset(preset_name, user_id)

    def _show_preset_info(self, preset_name, user_id):
        user_presets = UserData(user_id).gpt_presets.load()
        preset_found = None
        for preset in user_presets:
            if preset["name"] == preset_name:
                preset_found = preset
        about_preset_msg = (f"<b><u>Выбрано</u>: <code>{preset_found["name"]}</code>\n<u>Инструкция</u>: "
                            f"<code>{preset_found["instruction"]}</code></b>")
        reply_markup = ReplyKeyboards.get_user_presets_keyboard(user_id)
        sent_message = self.bot.send_message(user_id, about_preset_msg, parse_mode='HTML', reply_markup=reply_markup)
        self.bot.pin_chat_message(user_id, sent_message.message_id)

    def _make_active_preset(self, preset_name, user_id):
        userdata = UserData(user_id)
        cfg = userdata.config.load()
        cfg["gpt_active_preset"] = preset_name
        userdata.config.write(cfg)
        self._show_preset_info(preset_name, user_id)

    def register_handlers(self):
        self.bot.message_handler(func=lambda message: True)(self._text_handler)

    @classmethod
    def _check_if_preset_button(cls, preset_name, user_id):
        preset_name = cls._remove_active_status_str(preset_name)
        preset_list = UserData(user_id).gpt_presets.load()
        preset_names = [preset["name"] for preset in preset_list]
        if preset_name in preset_names:
            return True
        return False

    @staticmethod
    def _remove_active_status_str(text):
        text = str(text)
        if text[0:2] == BotData.ACTIVE_STATUS_STR:
            return text[2:]
        else:
            return text