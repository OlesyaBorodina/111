from loader import bot
from telebot.types import Message
from keyboards.reply_keyboards.help import help_keyboard


@bot.message_handler(commands=["start", "hello_world"])
def greetings(message: Message) -> None:
    """
    Функция-приветствие (команды /start и /hello_world)

    :param message: Объект сообщения
    :return message: Message
    :return: None
    """

    bot.send_message(message.chat.id, f"Привет, {message.from_user.full_name}!\nДобро пожаловать в Telegram-бот турагентства Too Easy Travel. "
                                      f"Я найду для тебя лучшие отели на сайте hotels.com (кроме России).\n"
                                      f"Чтобы начать, выбери команду или введи /help для справки!",
                                      reply_markup=help_keyboard())
