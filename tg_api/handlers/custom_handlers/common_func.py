import logging
import sys

from config_data.logger_config import *
import os.path
from contextlib import suppress
from typing import Generator

from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import Message, ReplyKeyboardRemove, InputMediaPhoto, CallbackQuery
from requests import ReadTimeout

from database.core import def_insert_data, def_get_elem, def_del_old_elem
from database.models.models import User, db, FilmsBase, Top100Films, Find_Film_Param
from database.utilits.common_func import create_list_for_find_film
from site_api.core import def_find_film, def_top_100_film, def_find_film_param
from tg_api.keyboards.inline.some_inline_kb import change_films_kb

from typing import Type

logger = logging.getLogger(f'main.tg_api.handlers.custom_handlers.{os.path.basename(__file__)}')
sys.excepthook = any_exception

user_data = {}
dict_with_films = {}


def photo_finder(num: int, user_id: int, out_message_dict: dict) -> str:
    """Поиск фото в списке результатов поиска"""
    logger.debug(f'{photo_finder.__name__} - начало работы')
    logger.debug(f"{photo_finder.__name__} - {out_message_dict[user_id][num]['poster'].get('previewUrl')}")
    logger.info(f'{photo_finder.__name__} - нашел фото')
    return out_message_dict[user_id][num]['poster'].get('previewUrl')


def caption(num: int, user_id: int, out_message_dict: dict) -> str:
    """Генерация описание картинки"""
    logger.debug(f'{caption.__name__} - начало поиска описания картинки')
    film_name = out_message_dict[user_id][num].get('name')
    alternative_name = out_message_dict[user_id][num].get('alternativeName')
    year = out_message_dict[user_id][num].get('year')
    genres = ','.join([el['name'] for el in out_message_dict[user_id][num].get('genres')])
    description = out_message_dict[user_id][num].get('description')
    rating = ', '.join(
        [f'{k}={round(v, 2)}' for k, v in out_message_dict[user_id][num].get('rating').items() if v is not None][0:2]
    )
    series_length = out_message_dict[user_id][num].get('seriesLength')
    movie_length = out_message_dict[user_id][num].get('movieLength')
    is_series = out_message_dict[user_id][num].get('isSeries')
    if is_series:
        photo_caption = (f'<b>{film_name}</b>\\<i>{alternative_name}</i>'
                         f'({year})\n'
                         f'<b>Жанры:</b> {genres}\n'
                         f'<b>Описание:</b> {description}\n'
                         f'<b>Рейтинг:</b>🏆{rating}\n'
                         f'Сериал\n'
                         f'Продолжительность серии: {series_length} минут')
    else:
        photo_caption = (f'<b>{film_name}</b>\\<i>{alternative_name}</i>'
                         f'({year})\n'
                         f'<b>Жанры:</b> {genres}\n'
                         f'<b>Описание:</b> {description}\n'
                         f'<b>Рейтинг:</b>🏆{rating}\n'
                         f'Фильм\n'
                         f'Продолжительность: {movie_length} минут')
    logger.info(f'{caption.__name__} - подготовил описание картинки')
    return photo_caption


def countries_list() -> Generator:
    """Генератор списка стран"""
    with open('country.txt', 'r', encoding='UTF-8') as file:
        for line in file.readlines():
            yield line.strip()


async def rez_finder(message: Message, state: FSMContext, new_state: State,
                     table: Type[FilmsBase | Top100Films | Find_Film_Param]):
    """Поиск фильмов и вывод результата в виде картинки с описанием и кнопками листания"""
    logger.debug(f'{rez_finder.__name__} - начало работы функции показывающей результаты поиска')
    user_inf = message.from_user.id
    st_name = await state.get_state()
    try:
        logger.debug(f'{rez_finder.__name__} - определяю необходимые настройки')
        if st_name == 'MovieSearch:choosing_film_name':
            old_elem = def_del_old_elem(db, user_inf, FilmsBase, User)
            response_list = def_find_film(message.text, limit_page=30)
            if isinstance(response_list, list) and len(response_list):
                out_list = create_list_for_find_film(User.get(User.user_id == user_inf), response_list, message.text)
                def_insert_data(db, table, out_list)
            elif isinstance(response_list, list):
                await message.answer('А я не знаю такой фильм 🤖')
                return
            else:
                logger.warning(f'{rez_finder.__name__} - {response_list}')
                await message.answer('Что то пошло не так ! Буду разбираться', reply_markup=ReplyKeyboardRemove())
                await message.answer_sticker('CAACAgIAAxkBAAELUIxlv4FmGKw0Z7rVlCfWSo1gTA_n1wACWQADJxRJC-OPDSX1raG1NAQ')
                await state.clear()
                return
        elif st_name == 'MovieSearch:choosing_top_100':
            old_elem = def_del_old_elem(db, None, Top100Films, None)
            if old_elem or len(Top100Films.select()) == 0:
                response_list = def_top_100_film()
                if isinstance(response_list, list) and len(response_list):
                    out_list = create_list_for_find_film(None, response_list, None)
                    def_insert_data(db, table, out_list)
                else:
                    logger.warning(f'{rez_finder.__name__} - {response_list}')
                    await message.answer('Что то пошло не так ! Буду разбираться', reply_markup=ReplyKeyboardRemove())
                    await message.answer_sticker(
                        'CAACAgIAAxkBAAELUIxlv4FmGKw0Z7rVlCfWSo1gTA_n1wACWQADJxRJC-OPDSX1raG1NAQ')
                    await state.clear()
        elif st_name == 'MovieSearch:choosing_find_film_param':
            old_elem = def_del_old_elem(db, user_inf, Find_Film_Param, User)
            logger.debug(f'{rez_finder.__name__} - {user_data}')
            response_list = def_find_film_param(*user_data[user_inf])
            if isinstance(response_list, list) and len(response_list):
                query_str = ','.join([el if el is not None else 'Все равно'
                                      for el in user_data[user_inf]])
                out_list = create_list_for_find_film(User.get(User.user_id == user_inf), response_list, query_str)
                def_insert_data(db, table, out_list)
            elif isinstance(response_list, list):
                await message.answer('А я не знаю такой фильм 🤖')
                return
            else:
                logger.warning(f'{rez_finder.__name__} - {response_list}')
                await message.answer('Что то пошло не так ! Буду разбираться', reply_markup=ReplyKeyboardRemove())
                await message.answer_sticker('CAACAgIAAxkBAAELUIxlv4FmGKw0Z7rVlCfWSo1gTA_n1wACWQADJxRJC-OPDSX1raG1NAQ')
                await state.clear()
                return
        if user_inf in dict_with_films:
            del dict_with_films[user_inf]
        if user_inf in user_data:
            del user_data[user_inf]
        if st_name == 'MovieSearch:choosing_film_name' or st_name == 'MovieSearch:choosing_find_film_param':
            dict_with_films[user_inf] = def_get_elem(db, user_inf, table, User)
        elif st_name == 'MovieSearch:choosing_top_100':
            dict_with_films[user_inf] = def_get_elem(db, user_inf, table, None)
        logger.debug(f'{rez_finder.__name__} - подготовлены данные для ответа')
        await message.answer_photo(
            photo=photo_finder(num=0, user_id=user_inf, out_message_dict=dict_with_films),
            caption=caption(num=0, user_id=user_inf, out_message_dict=dict_with_films),
            reply_markup=change_films_kb(num=0, all_num=len(dict_with_films[user_inf])))
        await state.set_state(new_state)
    except ReadTimeout as exs:
        logger.exception('сайт не отвечает', exc_info=True)
        await message.answer('Упсссс...Сервер не отвечает', reply_markup=ReplyKeyboardRemove())
        await message.answer_sticker('CAACAgIAAxkBAAELUIxlv4FmGKw0Z7rVlCfWSo1gTA_n1wACWQADJxRJC-OPDSX1raG1NAQ')


async def update_num_text(message: Message, new_value: int, user_id):
    """Обновление описания картинки"""
    logger.debug(f'{update_num_text.__name__} - начало работы')
    with suppress(TelegramBadRequest):
        photo = InputMediaPhoto(
            media=photo_finder(num=new_value, user_id=user_id, out_message_dict=dict_with_films),
            caption=caption(num=new_value, user_id=user_id, out_message_dict=dict_with_films))
        await message.edit_media(
            media=photo,
            reply_markup=change_films_kb(num=new_value, all_num=len(dict_with_films[user_id]))
        )
    logger.info(f'{update_num_text.__name__} - КОнец работы')


async def callbacks_num(callback: CallbackQuery, state: FSMContext, new_state: State):
    """Кнопки колбэки"""
    logger.debug(f'{callbacks_num.__name__} - начало работы')
    user_value = user_data.get(callback.from_user.id, 0)
    action = callback.data.split("_")[1]

    if action == "incr":
        user_data[callback.from_user.id] = (user_value + 1) % len(dict_with_films[callback.from_user.id])
        await update_num_text(callback.message, (user_value + 1) % len(dict_with_films[callback.from_user.id]),
                              callback.from_user.id)
    elif action == "decr":
        user_data[callback.from_user.id] = (user_value - 1) % len(dict_with_films[callback.from_user.id])
        await update_num_text(callback.message, (user_value - 1) % len(dict_with_films[callback.from_user.id]),
                              callback.from_user.id)
    await callback.answer(' ')
    await state.set_state(new_state)
    logger.info(f'{callbacks_num.__name__} - выполнил задачу')


if __name__ == '__main__':
    print('Nenm')
