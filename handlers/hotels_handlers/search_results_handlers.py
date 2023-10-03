from loader import bot
import json
from datetime import datetime
from telebot.types import CallbackQuery, InputMediaPhoto
from handlers.API_handlers import request_hotels
from handlers.API_handlers import request_photo
from states.travel_information import TravelInfoState
from database.history_db_methods import add_hotels_to_history_db
from keyboards.inline_keyboards.default_keyboard import default_keyboard
from keyboards.inline_keyboards.next_hotel import next_hotel_keyboard
from utils.show_hotels import show_hotel


@bot.callback_query_handler(func=lambda call: call.data.startswith('{'),
                            state=TravelInfoState.show_hotels)
def results_handler(callback: CallbackQuery) -> None:
    """
    Выдача отелей по одному.
    Сохранение выданных отелей в бд для истории поиска.

    :param callback: Объект CallBackQuery
    :type: CallbackQuery
    :return: None
    """
    chat_id = callback.message.chat.id
    bot.delete_message(chat_id, callback.message.id)

    callback_json = json.loads(callback.data)
    method = callback_json['method']
    page_num = callback_json['page_num']
    hotel_num = callback_json['hotel_num']

    with bot.retrieve_data(callback.from_user.id, chat_id) as data:
        if method == 'INIT':
            data['hotels_list'] = request_hotels(data, page_num)
        hotels_list = data['hotels_list']

    if hotels_list:
        hotels_list_length = len(hotels_list)

        if hotels_list_length == 0:
            bot.send_message(chat_id, 'К сожалению, по твоему запросу не найдено ни одного отеля\n'
                                      'Хочешь повторить поиск?',
                                      reply_markup=default_keyboard())

        elif hotels_list_length == hotel_num + 1 and hotel_num != 24: # количество отелей на странице
            bot.send_message(chat_id, 'Отелей больше нет. Хочешь повторить поиск?',
                                      reply_markup=default_keyboard())

        else:
            add_hotels_to_history_db(chat_id, hotels_list[hotel_num]['id'], hotels_list[hotel_num]['name'])
            show_hotel(hotels_list[hotel_num], chat_id)

            if hotel_num == 24: # количество отелей на странице
                page_num += 1
                hotel_num = 0
                with bot.retrieve_data(callback.from_user.id, chat_id) as data:
                    data['hotels_list'] = request_hotels(data, page_num)

            bot.send_message(chat_id, 'Показать ещё?',
                             reply_markup=next_hotel_keyboard('Ещё!', 'NEXT', page_num, hotel_num))

    else:
        bot.send_message(chat_id,
                         'Упс, кажется что-то пошло не так! Попробуй повторить поиск.\n'
                         'Если ошибка будет повторяться, свяжись с моим автором - @olbo72',
                         reply_markup=default_keyboard())

    bot.answer_callback_query(callback.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('PHOTO'))
def show_hotel_photo(callback: CallbackQuery) -> None:
    """
    Выдача фото отеля.

    :param callback: Объект CallBackQuery
    :type: CallbackQuery
    :return: None
    """

    hotel_id = int(callback.data.split('|')[1])
    # photos_list = request_photo(hotel_id)
    photos_dict = request_photo(hotel_id)
    address = photos_dict['addr']
    bot.send_message(callback.message.chat.id, f'Отель расположен по адресу: {address}')
    if photos_dict:
        media_list = []

        for i_photo in photos_dict['photo_url']:
            input_media = InputMediaPhoto(i_photo, caption='hi')
            media_list.append(input_media)

        bot.send_media_group(callback.message.chat.id, media_list)

    else:
        bot.send_message(callback.message.chat.id,
                         'Упс, кажется что-то пошло не так! Попробуй повторить поиск.\n'
                         'Если ошибка будет повторяться снова, свяжись с моим автором - @olbo72',
                         reply_markup=default_keyboard())
    bot.answer_callback_query(callback.id)


@bot.callback_query_handler(func=lambda call: call.data == 'HIDE',
                            state=TravelInfoState.show_hotels)
def hide_hotel(callback: CallbackQuery) -> None:
    """
    Удаление отеля из чата.

    :param callback: Объект CallBackQuery
    :type: CallbackQuery
    :return: None
    """

    bot.delete_message(callback.message.chat.id, callback.message.id)

    bot.answer_callback_query(callback.id)