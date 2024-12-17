from src.utils.user_data import UserData
from src.utils.bot_data import BotData
from src.keyboards.reply_keyboards import ReplyKeyboards


class TextHandler:

    def __init__(self, bot):
        self.bot = bot
        self._register_handlers()

    def _text_handler(self, message):
        # Если это текст из кнопок пресетов - обрабатываем нажатие на кнопку
        if self._check_if_preset_button(message.text, message.from_user.id):
            self._button_handler(message)
            return
        # Если любая команда - игнорируем
        elif message.text[0] == '/':
            return
        # Обычный текст - запрос в гпт
        else:
            pass

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
        about_preset_msg = (f"<b><u>Выбрано:</u>  <code>{preset_found["name"]}</code>\n<u>Инструкция:</u> \n"
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


    def _register_handlers(self):
        self.bot.message_handler(func=lambda message: True)(self._text_handler)

    @classmethod
    def _check_if_preset_button(cls, preset_name, user_id):
        text = cls._remove_active_status_str(preset_name)
        user_presets = UserData(user_id).gpt_presets.load()
        for preset in user_presets:
            if preset["name"] == text:
                return True
        return False

    @staticmethod
    def _remove_active_status_str(text):
        text = str(text)
        if text[0:2] == BotData.ACTIVE_STATUS_STR:
            return text[2:]
        else:
            return text