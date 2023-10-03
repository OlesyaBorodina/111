import requests
from requests.models import Response
from typing import Optional
from logger_config import logger


@logger.catch
def connect_rapid_api_post(url: str, header: dict, req_params: dict) -> Optional[Response]:
    """
    Установка соединения с API Hotels.com.
    :param url: ссылка на эндпойнт
    :type url: str
    :param header: хэдер запроса. Содержит ключ API
    :type header: dict
    :param req_params: параметры запроса
    :type req_params: dict
    :return: response
    :rtype: Response
    """

    response = requests.request("POST", url, json=req_params, headers=header, timeout=10)

    if response.status_code == requests.codes.ok:
        return response
    else:
        raise ConnectionError(f'Возникли проблемы с подключением к API. Код ответа: {response.status_code}')
