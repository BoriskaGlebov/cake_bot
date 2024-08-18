# модуль с функцие которая готовит список для добавления в таблицу с БД
from pprint import pprint
from typing import TypeVar
from typing import Union, List, Dict
from datetime import datetime

T = TypeVar('T')


def create_list_for_find_film(user_inst: T | None, film_response: Union[List[Dict]], query: str | None) -> List[Dict]:
    """
    Делаю окончательный словарь для добавления в таблицу с фильмам
    :param user_inst: Данные пользователя
    :param film_response: ответ с запроса
    :param query: сам запрос
    :return: словарь для добавления в БД
    """
    out_list = []
    for num, elem in enumerate(film_response):
        if elem.get('name') and elem.get('description') and elem.get('poster'):
            elem['film_id'] = elem.pop('id')
        else:
            continue
        if query is not None and user_inst is not None:
            elem['query'] = query
            elem['user'] = user_inst
        out_list.append(elem)
    return out_list
