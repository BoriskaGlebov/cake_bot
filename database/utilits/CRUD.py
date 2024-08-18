# Модуль реализует основные функции работы с БД
import logging
import sys
import time
from logging import config
from pprint import pprint

from config_data.logger_config import *
import os
from datetime import datetime, timedelta

from typing import TypeVar, List, Dict

from peewee import SqliteDatabase

from database.models.models import *  # для тестов
from site_api.core import *
from database.utilits.common_func import create_list_for_find_film

logger = logging.getLogger(f'main.database.utilits.{os.path.basename(__file__)}')
sys.excepthook = any_exception
# logging.config.dictConfig(dict_config) #только на момент тестирования функций нужно
T = TypeVar('T')


def _insert_single_user(model: T, user_id: int, user_name: str = 'Guest_User'):
    """
    Добавление пользователя в БД
    :param model: название таблицы
    :param user_id: id пользователя
    :param user_name: имя пользователя если оно есть
    :return: None
    """
    logger.debug(f'{_insert_single_user.__name__} - начало работы')
    user = model.select().where(model.user_id == user_id)
    if len(user):
        logger.info(f'{_insert_single_user.__name__} - такой пользователь уже в БД')
    else:
        user = model.create(user_id=user_id, user_name=user_name)
        logger.info(f'{_insert_single_user.__name__} - Добавил {user_name}')
    return user


def _insert_data(database: SqliteDatabase, model: T, data: List[Dict]) -> None:
    """
    Вставка всех элементов в базу данных
    :param database: База данных
    :param model: название таблицы
    :param data: данные для добавления в таблицу
    :return: None
    """
    logger.debug(f'{_insert_data.__name__} - начало работы')
    with database.atomic():
        logger.debug(f'{_insert_data.__name__} - осуществляю добавление данных в {model}')
        model.insert_many(data).execute()
    logger.info(f'{_insert_data.__name__} -Данные добавлены в таблицу {model}')
    return None


def _retrieve_elem(database: SqliteDatabase, user_id: int, model_film: T, model_user: T | None) -> list[dict]:
    """
    Извлечение в список последних фильмов которые пользователь спрашивал
    :param database: База данных
    :param user_id: ID пользователя
    :param model_film: Таблица из которой будут извлекать данные
    :param model_user: инстанс пользователя из БД
    :return: список строк БД
    """
    logger.debug(f'{_retrieve_elem.__name__} - начало работы')
    if user_id is not None and model_user is not None:
        last_query_time = model_film.select(model_film.created_at).join(model_user).where(
            model_user.user_id == user_id).order_by(-model_film.created_at).limit(1)[0].created_at
        logger.debug(f'{_retrieve_elem.__name__} - Узнал время последнего запроса')
        with (database.atomic()):
            logger.debug(f'{_retrieve_elem.__name__} - получаю данные из таблицы {model_film}')
            response = model_film.select(model_film).join(model_user).where(
                model_user.user_id == user_id, model_film.created_at == last_query_time).dicts()
            logger.info(f'{_retrieve_elem.__name__} - Данные получены из таблицы {model_film}')

    else:
        with (database.atomic()):
            logger.debug(f'{_retrieve_elem.__name__} - получаю данные из таблицы {model_film}')
            response = model_film.select().dicts()
            logger.info(f'{_retrieve_elem.__name__} - Данные получены из таблицы {model_film}')

    return response


def _del_instance(database: SqliteDatabase, user_id: int | None, model_film: T, model_user: T | None):
    """
    Удаляет элементы в таблице если прошло больше какого-то времени
    :param database: БД
    :param user_id: ID пользователя
    :param model_film: название таблицы
    :param model_user: инстанс пользователя
    :return: список фильмов под удаление
    """
    logger.debug(f'{_del_instance.__name__} - начало работы')
    result_db = []
    with database.atomic():
        if user_id is None:
            logger.debug(f'{_del_instance.__name__} - поиск строк для удаления {model_film}')
            result_db = model_film.select().where(model_film.created_at < datetime.now() - timedelta(minutes=15))
        else:
            logger.debug(f'{_del_instance.__name__} - поиск строк для удаления {model_film}')
            result_db = model_film.select().join(model_user).where(model_user.user_id == user_id,
                                                                   model_film.created_at < datetime.now() - timedelta(
                                                                       minutes=15))
        if result_db:
            for el in result_db:
                el.delete_instance()
                logger.debug(f'{_del_instance.__name__} - Удаляю старые строчки')
            logger.info(f'{_del_instance.__name__} - старые строки удалены')
            return result_db
        else:
            logger.info(f'{_del_instance.__name__} - удалять было нечего')
            return result_db


class CRUDInterface:
    """Создание, чтение, обновление, удаление данных в БД"""

    @classmethod
    def insert_single_user(cls):
        """
        Возвращает функцию _insert_single_user
        :return: функция
        """
        return _insert_single_user

    @classmethod
    def insert_data(cls):
        """
        Возвращает функцию _insert_data
        :return: функция
        """
        return _insert_data

    @classmethod
    def retrieve_elem(cls):
        """
        Возвращает функцию _retrieve_elem
        :return: функция
        """
        return _retrieve_elem

    @classmethod
    def del_old_el(cls):
        """
        Возвращает функцию _del_instance
        :return: функция
        """
        return _del_instance


if __name__ == '__main__':
    user = _insert_single_user(User, 123, 'Test_User')
    print(user)
    # find_film = def_find_film('1+1')
    # ins_data = create_list_for_find_film(user, find_film, '1+1')
    # _insert_data(db, FilmsBase, ins_data)
    # retr_elem = _retrieve_elem(db, 123, FilmsBase, User)
    # pprint(retr_elem)
    # del_inst = _del_instance(db, 123, FilmsBase, User)
    # print(del_inst)
    # user.delete_instance(recursive=True)
