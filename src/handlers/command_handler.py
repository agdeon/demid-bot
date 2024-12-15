class CommandHandler:
    START_MSG = ("Этот бот позволяет создавать разные пресеты GPT с кастомными заранее заданными инструкциями. Список "
                 "команд также доступен в боковом меню команд. Выбрать нужный пресет можно в меню кнопок бота.\n"
                 "/start - рестарт бота\n"
                 "/create - создать пресет\n"
                 "/remove - удалить текущий выбранный пресет\n"
                 "/help - подробная информация\n"
                 "/stats - ваша статистика\n")

    def __init__(self, bot):
        self.bot = bot

    def start(self, message):
        self.bot.send_message(message.chat.id, self.START_MSG)

    def create(self, message):
        pass

    def remove(self, message):
        pass


    def help(self, message):
        self.bot.send_message(message.chat.id, "Это справка по использованию бота.")

    def stats(self, message):
        pass

    def register_handlers(self):
        self.bot.message_handler(commands=['start'])(self.start)
        self.bot.message_handler(commands=['create'])(self.create)
        self.bot.message_handler(commands=['remove'])(self.remove)
        self.bot.message_handler(commands=['help'])(self.help)
        self.bot.message_handler(commands=['stats'])(self.stats)