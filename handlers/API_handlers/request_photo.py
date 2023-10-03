import json
import re
from typing import List, Optional, Dict
from loader import rapid_api
from logger_config import logger
import requests
from . import connect_rapid_api_post


@logger.catch
def request_photo(hotel_id: int) -> Optional[Dict]:
    """Запрашивает с API фото и адрес, возвращает словарь ключи:
    addr - адрес отеля
    photo_url - список ссылок на фото отеля
    """
    prop_id = str(hotel_id)
    req_params = {
        "currency": "RUB",
        "eapid": 1,
        "locale": "ru_RUS",
        "siteId": 300000001,
        "propertyId": prop_id
    }

    response = connect_rapid_api_post('https://hotels4.p.rapidapi.com/properties/v2/get-summary', rapid_api, req_params)

    if response:
        resp_json = json.loads(response.text)

        hotel_images = resp_json['data']['propertyInfo']['propertyGallery']['images']
        hotel_images_length = len(hotel_images)

        photos_links = []
        summary_dict = dict()

        for elem in range(0, 10):
            if elem > hotel_images_length:
                break

            base_url = hotel_images[elem]['image']['url']
            photo_url = re.sub(r'{size}', 'y', base_url)
            photos_links.append(photo_url)
            elem += 1
        summary_dict['addr'] = resp_json['data']['propertyInfo']['summary']['location']['address'].get('addressLine')
        summary_dict['photo_url'] = photos_links
        return summary_dict
