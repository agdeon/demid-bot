from telebot.types import (KeyboardButton, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)

from src.utils.bot_data import BotData
from src.utils.user_data import UserData


class ReplyKeyboards:

    @staticmethod
    def get_user_presets_keyboard(user_id):
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        userdata = UserData(user_id)
        active_preset_name = userdata.config.load()["gpt_active_preset"]
        preset_list = userdata.gpt_presets.load()
        if len(preset_list) == 0:
            return ReplyKeyboardRemove()
        for preset in preset_list:
            preset_name = preset["name"]
            if preset_name == active_preset_name:
                preset_name = BotData.ACTIVE_STATUS_STR + preset_name
            markup.row(KeyboardButton(preset_name))
        return markup


