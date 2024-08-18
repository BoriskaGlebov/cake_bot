# Модуль основных функций с сайта Kinopoisk
import logging
import sys
from logging import config
from config_data.logger_config import *
import os.path
from typing import Dict, Any, Union, Callable, List, AnyStr
from requests import get
from site_api.settings.site_settings import headers_dict, status_code
from site_api.utils.common_func import column_names

logger = logging.getLogger(f'main.site_api.utils.{os.path.basename(__file__)}')
sys.excepthook = any_exception


# logging.config.dictConfig(dict_config)  # это на период тестирования


# @column_names
def _find_film(query_str: str, timeout: Any = 3, limit_page: int = 20, ) -> Union[List[Dict], AnyStr] | int:
    """
    Поиск фильма по названию и возвращает ответ в формате списка словарей с фильмами,
    так же может вернуть ключи словаря с типом данных пригодным для
    подготовки таблицы в БД
    :param query_str: название фильма
    :param timeout: прерывание запроса через секунд
    :param limit_page: количество выводимых фильмов
    :return: response: ответ с сайта в формате json или код ошибки
    """
    logger.debug(f'{_find_film.__name__} - Запуск функции поиска фильмов')
    url = 'https://api.kinopoisk.dev/v1.4/movie/search?'
    param = {'page': 1, 'limit': limit_page, 'query': query_str}
    response = get(url, params=param, headers=headers_dict, timeout=timeout)
    logger.debug(f'{_find_film.__name__} - Получил данные для работы')
    if response.status_code == 200:
        logger.info(_find_film.__name__ + " - " + status_code.get(response.status_code))
        return response.json()['docs']
    else:
        logger.error(f'{_find_film.__name__} - Что-то пошло не так! '
                     f'Код = {response.status_code} = {status_code.get(response.status_code)}')
        return response.status_code


# @column_names
def _find_100_film(timeout: Any = 5, limit_page: int = 100, ) -> Union[Dict, str] | int:
    """
    Поиск топ 100 фильмов Кинопоискаи возвращает ответ в формате списка словарей с фильмами,
    так же может вернуть ключи словаря с типом данных пригодным для
    подготовки таблицы в БД
    :param timeout: прерывание запроса через секунд
    :param limit_page: количество выводимых фильмов
    :return: ответ с сайта в формате json или код ошибки
    """
    logger.debug(f'{_find_100_film.__name__} - Запуск функции топ 100 фильмов')
    url = 'https://api.kinopoisk.dev/v1.4/movie?'
    param = {'page': 1, 'limit': limit_page,
             'selectFields': ['id', 'name', 'alternativeName', 'year', 'genres', 'description',
                              'rating', 'movieLength', 'poster', 'videos', 'networks', ],
             'notNullFields': 'id',
             'sortField': 'rating.kp', 'sortType': '-1', 'lists': 'top250'}
    response = get(url, params=param, headers=headers_dict, timeout=timeout)
    logger.debug(f'{_find_100_film.__name__} - Получил данные для работы')
    if response.status_code == 200:
        logger.info(_find_100_film.__name__ + " - " + status_code.get(response.status_code))
        return response.json()['docs']
    else:
        logger.error(f'{_find_100_film.__name__} - Что-то пошло не так! '
                     f'Код = {response.status_code} = {status_code.get(response.status_code)}')
        return response.status_code


# @column_names
def _find_film_param(film_types: str | None = None, years: str | None = None,
                     rating_kp: str | None = None, genres: str | None = None,
                     countries: str | None = None,
                     limit_page: int = 20,
                     timeout: Any = 10, ) -> Union[Dict, str] | int:
    """
    Поиск фильмов и сериалов по параметрам Кинопоиска возвращает ответ в формате списка словарей с фильмами,
    так же может вернуть ключи словаря с типом данных пригодным для
    подготовки таблицы в БД
    :param film_types: movie,tv-series,cartoon,animated-series,anime или !anime
    :param years: 1874, 2050, !2020, 2020-2024
    :param rating_kp: 7, 10, 7.2-10
    :param genres: "драма", "комедия", "!мелодрама", "+ужасы"
    :param countries: "США", "Россия", "!Франция" , "+Великобритания"
    :param limit_page: количество выводимых фильмов
    :param timeout: прерывание запроса через секунд
    :return: ответ с сайта в формате json или код ошибки
    """
    logger.debug(f'{_find_100_film.__name__} - Запуск функции поиск фильмов по параметрам')
    url = 'https://api.kinopoisk.dev/v1.4/movie?'
    param = {'page': '1', 'limit': limit_page, 'selectFields': '',
             'notNullFields': ['id', 'name', 'alternativeName', 'description', 'type', 'year', ]}
    keys = ['type', 'year', 'rating.kp', 'genres.name', 'countries.name']
    values = [film_types, years, rating_kp, genres, countries]
    param_user = {keys[num]: el for num, el in enumerate(values) if el is not None}
    param.update(param_user)
    response = get(url, params=param, headers=headers_dict, timeout=timeout)
    logger.debug(f'{_find_film_param.__name__} - Получил данные для работы')
    if response.status_code == 200:
        logger.info(_find_film_param.__name__ + " - " + status_code.get(response.status_code))
        return response.json()['docs']
    else:
        logger.error(f'{_find_film_param.__name__} - Что-то пошло не так! '
                     f'Код = {response.status_code} = {status_code.get(response.status_code)}')
        return response.status_code


class SiteApiInterface:
    """
    Интерфейс поиска фильмов
    """

    @classmethod
    def film_finder(cls) -> Callable:
        """
        Возвращает функцию _find_film
        :return: функция
        """
        return _find_film

    @classmethod
    def top_100_film(cls) -> Callable:
        """
        Возвращает функцию _find_100_film
        :return: функция
        """
        return _find_100_film

    @classmethod
    def find_film_param(cls) -> Callable:
        """
        Возвращает функцию _find_film_param
        :return: функция
        """
        return _find_film_param


if __name__ == '__main__':
    # headers_dict = {}
    res = _find_film('1+1')
    # print(res)

    res2 = _find_100_fil()
    # print(res2)
    # #
    res3 = _find_film_param('movie')
    # print(res)
    # pass
