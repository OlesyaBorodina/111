import json
from typing import Dict, Optional
from . import connect_rapid_api
from loader import rapid_api
from logger_config import logger


@logger.catch
def request_location(location_group: str, location: str) -> Optional[Dict]:
    """
    Принимает на вход строку и возвращает словарь с ID наиболее близких к введённой строке локаций.
    Если возникли проблемы с подключением к API, возвращает сообщение об ошибке.
    :param location_group: группа, в которой ищем локацию
    :type location_group: str
    :param location: локация, указанная пользователем
    :type location: str
    :return: locations_id или None
    :rtype: Dict[str]
    """

    req_params = {"q": location, "locale": "ru_RU", "langid": "1033", "siteid": "300000001"}
    response = connect_rapid_api('https://hotels4.p.rapidapi.com/locations/v3/search', rapid_api, req_params)

    if response:
        resp_json = json.loads(response.text)

        locations_dict = {}
        for region in resp_json['sr']:

            for key, value in region.items():
                if value == location_group:
                    city_name = region['regionNames'].get('fullName')
                    city_id = region['gaiaId']
                    locations_dict[city_name] = city_id

        return locations_dict