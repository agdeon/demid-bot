from src.utils.user_data import UserData
from src.keyboards.reply_keyboards import ReplyKeyboards
from src.utils.bot_data import BotData


class CommandHandler:
    # Все сообщения в формате parse_mode='HTML'

    def __init__(self, bot):
        self.bot = bot
        self._register_handlers()

    def start(self, message):
        start_msg = ("<b>Этот бот позволяет создавать разные пресеты GPT, с кастомными, заранее заданными инструкциями. Список "
                 "команд также доступен в боковом меню команд. Выбрать нужный пресет можно в меню кнопок бота\n"
                 "\n"
                 "/start - рестарт бота\n"
                 "/create - создать пресет\n"
                 "/remove - удалить текущий выбранный пресет\n"
                 "/help - подробная информация\n"
                 "/stats - ваша статистика</b>\n")

        reply_markup = ReplyKeyboards.get_user_presets_keyboard(message.chat.id)
        self.bot.send_message(message.chat.id, start_msg, parse_mode='HTML', reply_markup=reply_markup)

    def create(self, message):
        enter_preset_name_msg = "<b>Введите имя для нового пресета GPT</b>"
        self.bot.send_message(message.chat.id, enter_preset_name_msg, parse_mode='HTML')
        self.bot.register_next_step_handler(message, self.preset_name_input)


    # Sessions handlers
    def preset_name_input(self, message):
        if self._is_command(message.text) or self._is_button(message.text, message.from_user.id):
            return

        name = message.text
        if len(name) > 25:
            name = name[0:25]

        enter_instruction_msg = f"<b>Теперь напишите инструкцию для вашего пресета</b>"
        self.bot.send_message(message.chat.id, enter_instruction_msg, parse_mode='HTML')
        self.bot.register_next_step_handler(message, self.preset_instruction_input, name)

    def preset_instruction_input(self, message, name):
        if self._is_command(message.text) or self._is_button(message.text, message.from_user.id):
            return

        userdata = UserData(message.chat.id)
        gpt_presets = userdata.gpt_presets.load()
        gpt_presets.append({"name": name, "instruction": message.text})
        userdata.gpt_presets.write(gpt_presets)
        success_msg = f"<b>Пресет <code>{name}</code> успешно создан и сохранен! Теперь он доступен в меню</b>"
        repl_markup = ReplyKeyboards.get_user_presets_keyboard(message.from_user.id)
        self.bot.delete_state(message.from_user.id, message.chat.id)
        self.bot.send_message(message.chat.id, success_msg, parse_mode='HTML', reply_markup=repl_markup)


    def remove(self, message):
        pass


    def help(self, message):
        self.bot.send_message(message.chat.id, "Это справка по использованию бота.")

    def stats(self, message):
        pass

    @staticmethod
    def _is_command(text):
        if text[0] == '/':
            return True
        return False

    @staticmethod
    def _is_button(text, user_id):
        if text[0:2] == BotData.ACTIVE_STATUS_STR:
            text = text[2:]
        user_presets = UserData(user_id).gpt_presets.load()
        for preset in user_presets:
            if preset["name"] == text:
                return True
        return False


    def _register_handlers(self):
        self.bot.message_handler(commands=['start'])(self.start)
        self.bot.message_handler(commands=['create'])(self.create)
        self.bot.message_handler(commands=['remove'])(self.remove)
        self.bot.message_handler(commands=['help'])(self.help)
        self.bot.message_handler(commands=['stats'])(self.stats)