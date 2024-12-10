class CommandHandler:
    def __init__(self, bot):
        self.bot = bot

    def start(self, message):
        self.bot.send_message(message.chat.id, "Привет! Это команда /start.")

    def help(self, message):
        self.bot.send_message(message.chat.id, "Это справка по использованию бота.")

    def register_handlers(self):
        self.bot.message_handler(commands=['start'])(self.start)
        self.bot.message_handler(commands=['help'])(self.help)