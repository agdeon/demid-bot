from telebot.types import ReplyKeyboardMarkup, KeyboardButton


class PresetListKeyboard:
    def __init__(self, presets_provider):
        self.presets_provider = presets_provider

    def generate_keyboard(self, user_id):
        presets = self.presets_provider(user_id)
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        for preset in presets:
            keyboard.add(KeyboardButton(text=preset["name"]))
        return keyboard
