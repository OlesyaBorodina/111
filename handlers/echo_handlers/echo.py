from loader import bot
from telebot.types import Message


@bot.message_handler(content_types=['text'], state=None)
def echo(message: Message) -> None:
    """
    Функция реакции на сообщение, не являющееся командой.

    :param message: Объект сообщения.
    :type message: Message
    :return: None
    """

    if message.text.lower().startswith('прив'):
        bot.send_message(message.chat.id,
                         f"Привет, {message.from_user.full_name}!\nДобро пожаловать в Telegram-бот турагентства Too Easy Travel. "
                                      f"Я найду для тебя лучшие отели на сайте hotels.com (кроме России).\n"
                                      f"Чтобы узнать, что я умею, введи /help")
    else:
        bot.send_message(message.chat.id,
                         f"Привет, {message.from_user.full_name}!\nК сожалению, я не понимаю человеческую речь.\n"
                         f"Но зато могу помочь найти лучшие отели!\n "
                         f"Введи /help, чтобы узнать больше!")