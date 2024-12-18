from src.keyboards.reply_keyboards import ReplyKeyboards
from src.utils.bot_data import BotData
from src.utils.user_data import UserData


class CommandHandler:
    # Все сообщения в формате parse_mode='HTML'

    def __init__(self, bot):
        self.bot = bot

    def start(self, message):
        start_msg = ("<b>Этот бот позволяет создавать разные пресеты GPT, с кастомными, заранее заданными инструкциями. Список "
                 "команд также доступен в боковом меню команд. Выбрать нужный пресет можно в меню кнопок бота\n"
                 "\n"
                 "/start - рестарт бота\n"
                 "/create - создать пресет\n"
                 "/remove - удалить текущий выбранный пресет\n"
                 "/help - подробная информация\n"
                 "/stats - ваша статистика</b>")

        reply_markup = ReplyKeyboards.get_user_presets_keyboard(message.chat.id)
        self.bot.send_message(message.chat.id, start_msg, parse_mode='HTML', reply_markup=reply_markup)

    def history(self, message):
        userdata = UserData(message.from_user.id)
        cfg = userdata.config.load()
        history_enabled = cfg["gpt_history_enabled"]
        if history_enabled:
            history_status_msg = '<b>🔴 История GPT <u>выключена</u>!</b>'
            cfg["gpt_history_enabled"] = False
        else:
            history_status_msg = '<b>🟢 История GPT была <u>активирована</u>!</b>'
            cfg["gpt_history_enabled"] = True
        userdata.config.write(cfg)
        self.bot.send_message(message.chat.id, history_status_msg, parse_mode='HTML')

    def create(self, message):
        enter_preset_name_msg = "<b>Введите имя для нового пресета GPT</b>"
        self.bot.send_message(message.chat.id, enter_preset_name_msg, parse_mode='HTML')
        self.bot.register_next_step_handler(message, self._preset_name_input)

    def _preset_name_input(self, message):
        name = message.text
        if not self._validate_preset_name(user_id=message.from_user.id,preset_name=name):
            invalid_data_msg = "<b>Некорректное имя пресета! Попробуйте еще раз.</b>"
            self.bot.send_message(message.chat.id, invalid_data_msg, parse_mode='HTML')
            self.bot.register_next_step_handler(message, self._preset_name_input)
            return

        if len(name) > 25:
            name = name[0:25]

        enter_instruction_msg = f"<b>Теперь напишите инструкцию для вашего пресета</b>"
        self.bot.send_message(message.chat.id, enter_instruction_msg, parse_mode='HTML')
        self.bot.register_next_step_handler(message, self._preset_instruction_input, name)

    def _preset_instruction_input(self, message, name):
        if self._is_command(message.text) or self._is_button(message.text, message.from_user.id):
            invalid_data_msg = "<b>Некорректные данные! Попробуйте еще раз.</b>"
            self.bot.send_message(message.chat.id, invalid_data_msg, parse_mode='HTML')
            self.bot.register_next_step_handler(message, self._preset_instruction_input, name)
            return

        userdata = UserData(message.chat.id)
        gpt_presets = userdata.gpt_presets.load()
        gpt_presets.append({"name": name, "instruction": message.text})
        userdata.gpt_presets.write(gpt_presets)
        success_msg = f"<b>Пресет <code>{name}</code> успешно создан и сохранен! Теперь он доступен в меню</b>"
        repl_markup = ReplyKeyboards.get_user_presets_keyboard(message.from_user.id)
        self.bot.send_message(message.chat.id, success_msg, parse_mode='HTML', reply_markup=repl_markup)

    def remove(self, message):
        userdata = UserData(message.chat.id)
        active_preset_name = userdata.config.load()["gpt_active_preset"]
        if not active_preset_name:
            no_preset_msg = "<b>Вы не выбрали пресет для удаления! Выберите нужный пресет в меню, затем повторите команду</b>"
            self.bot.send_message(message.chat.id, no_preset_msg, parse_mode='HTML')
        else:
            presets_list = userdata.gpt_presets.load()
            for i in range(len(presets_list)):
                if presets_list[i]["name"] == active_preset_name:
                    presets_list.pop(i)
                    userdata.gpt_presets.write(presets_list)
                    cfg = userdata.config.load()
                    cfg["gpt_active_preset"] = None
                    userdata.config.write(cfg)
                    break
            preset_deleted_msg = f"<b>Пресет <code>{active_preset_name}</code> был успешно удален</b>"
            repl_markup = ReplyKeyboards.get_user_presets_keyboard(message.from_user.id)
            self.bot.send_message(message.chat.id, preset_deleted_msg, parse_mode='HTML', reply_markup=repl_markup)

    def help(self, message):
        help_msg = ("<b><u>Cправка по использованию бота</u></b>\n\n"
                    "Этот бот позволяет создавать заранее настроенные GPT пресеты с кастомными инструкциями и "
                    "переключаться между ними.\n\n"
                    "В боте есть два меню, меню команд и меню пресетов. Меню команд находится слева от поля ввода, там "
                    "вы можете выбрать все доступные команды. Для выбора активного пресета используйте меню кнопок "
                    "которое находится справа от поля ввода.\n\n"
                    "Для того чтобы создать новый пресет, используйте команду /create\n"
                    "Чтобы удалить пресет, для начала выберите его в меню, затем используйте /remove\n"
                    "Для активации истории используйте /history\n")
        self.bot.send_message(message.chat.id, help_msg, parse_mode='HTML')

    def stats(self, message):
        stats_dict = UserData(message.from_user.id).stats.load()
        stats_data = ''
        for key, value in stats_dict.items():
            stats_data += f"{key}: {value}\n"
        stats_msg = f"<b><u>Ваша статистика</u></b>\n" + stats_data
        self.bot.send_message(message.chat.id, stats_msg, parse_mode='HTML')

    @staticmethod
    def _is_command(text):
        if text[0] == '/':
            return True
        return False

    @staticmethod
    def _is_button(text, user_id):
        if text[0:2] == BotData.ACTIVE_STATUS_STR:
            text = text[2:]
        preset_names = [preset["name"] for preset in UserData(user_id).gpt_presets.load()]
        if text in preset_names:
            return True
        return False

    @staticmethod
    def _validate_preset_name(*, user_id, preset_name):
        if preset_name[0:2] == BotData.ACTIVE_STATUS_STR:
            preset_name = preset_name[2:]
        if preset_name[0] == '/':
            return False
        preset_names = [preset["name"] for preset in UserData(user_id).gpt_presets.load()]
        if preset_name in preset_names:
            return False
        return True


    def register_handlers(self):
        self.bot.message_handler(commands=['start'])(self.start)
        self.bot.message_handler(commands=['history'])(self.history)
        self.bot.message_handler(commands=['create'])(self.create)
        self.bot.message_handler(commands=['remove'])(self.remove)
        self.bot.message_handler(commands=['help'])(self.help)
        self.bot.message_handler(commands=['stats'])(self.stats)