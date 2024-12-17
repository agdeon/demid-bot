class CallbackQueryHandler:
    def __init__(self, bot):
        self.bot = bot
        self._register_handlers()

    def handle_callback(self, call):
        if call.data == "button1":
            self.bot.answer_callback_query(call.id, "Нажата кнопка 1")
        elif call.data == "button2":
            self.bot.answer_callback_query(call.id, "Нажата кнопка 2")

    def _register_handlers(self):
        self.bot.callback_query_handler(func=lambda call: True)(self.handle_callback)