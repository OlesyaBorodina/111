from loader import bot
from telebot.types import Message
from keyboards.reply_keyboards.help import help_keyboard


@bot.message_handler(commands=['help'])
def help_command(message: Message) -> None:
    """
    Функция справка (команда /help)

    :param message: Объект сообщения.
    :type message: Message
    :return: None
    """

    bot.send_message(message.chat.id, "Вот, что я умею:\n"
                                      "/lowprice: покажу топ самых дешевых отелей по выбранному направлению\n"
                                      "/highprice: покажу топ самых дорогих отелей по выбранному направлению\n"
                                      "/bestdeal: покажу топ предложений по твоему запросу (близость к центру/цена)\n"
                                      "/favorites: покажу избранные отели\n"
                                      "/history: выдам историю твоего поиска\n"
                                      "/help: повторный вывод справки по командам", reply_markup=help_keyboard())
