from telebot import types


def default_keyboard() -> types.InlineKeyboardMarkup:
    """
    Создаёт клавиатуру для остановки и/или перезапуска поиска

    :return: keyboard
    :rtype: InlineKeyboardMarkup
    """

    keyboard = types.InlineKeyboardMarkup(row_width=1)

    try_again = types.InlineKeyboardButton(text='Начать сначала', callback_data='TRY_AGAIN')
    stop_search = types.InlineKeyboardButton(text='Прервать поиск', callback_data='CANCEL')

    keyboard.add(try_again)
    keyboard.add(stop_search)

    return keyboard
