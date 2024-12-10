class MessageHandler:
    def __init__(self, bot):
        self.bot = bot

    # Просто дублировние сообщения
    def echo(self, message):
        self.bot.send_message(message.chat.id, f"Вы написали: {message.text}")

    def register_handlers(self):
        self.bot.message_handler(content_types=['text'])(self.echo)