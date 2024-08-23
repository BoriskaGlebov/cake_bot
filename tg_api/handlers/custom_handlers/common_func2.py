import logging
import sys

from sqlalchemy.util import await_only

from config_data.config import site_tg_settings
from config_data.logger_config import *
import os.path
from contextlib import suppress
from typing import Generator

from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import Message, ReplyKeyboardRemove, InputMediaPhoto, CallbackQuery
from requests import ReadTimeout

# from database.core import def_insert_data, def_get_elem, def_del_old_elem
# from database.models.models import User, db, FilmsBase, Top100Films, Find_Film_Param
# from database.utilits.common_func import create_list_for_find_film
# from site_api.core import def_find_film, def_top_100_film, def_find_film_param

from site_api.site_api_func import SiteApiInterface
from tg_api.keyboards.inline.some_inline_kb import change_films_kb

from typing import Type

logger = logging.getLogger(f'main.tg_api.handlers.custom_handlers.{os.path.basename(__file__)}')
sys.excepthook = any_exception

photos_links = []
user_value=0


#
def photo_finder():
    return


#
#
# def caption(num: int, user_id: int, out_message_dict: dict) -> str:
#     """Генерация описание картинки"""
#     logger.debug(f'{caption.__name__} - начало поиска описания картинки')
#     film_name = out_message_dict[user_id][num].get('name')
#     alternative_name = out_message_dict[user_id][num].get('alternativeName')
#     year = out_message_dict[user_id][num].get('year')
#     genres = ','.join([el['name'] for el in out_message_dict[user_id][num].get('genres')])
#     description = out_message_dict[user_id][num].get('description')
#     rating = ', '.join(
#         [f'{k}={round(v, 2)}' for k, v in out_message_dict[user_id][num].get('rating').items() if v is not None][0:2]
#     )
#     series_length = out_message_dict[user_id][num].get('seriesLength')
#     movie_length = out_message_dict[user_id][num].get('movieLength')
#     is_series = out_message_dict[user_id][num].get('isSeries')
#     if is_series:
#         photo_caption = (f'<b>{film_name}</b>\\<i>{alternative_name}</i>'
#                          f'({year})\n'
#                          f'<b>Жанры:</b> {genres}\n'
#                          f'<b>Описание:</b> {description}\n'
#                          f'<b>Рейтинг:</b>🏆{rating}\n'
#                          f'Сериал\n'
#                          f'Продолжительность серии: {series_length} минут')
#     else:
#         photo_caption = (f'<b>{film_name}</b>\\<i>{alternative_name}</i>'
#                          f'({year})\n'
#                          f'<b>Жанры:</b> {genres}\n'
#                          f'<b>Описание:</b> {description}\n'
#                          f'<b>Рейтинг:</b>🏆{rating}\n'
#                          f'Фильм\n'
#                          f'Продолжительность: {movie_length} минут')
#     logger.info(f'{caption.__name__} - подготовил описание картинки')
#     return photo_caption

#
# def countries_list() -> Generator:
#     """Генератор списка стран"""
#     with open('country.txt', 'r', encoding='UTF-8') as file:
#         for line in file.readlines():
#             yield line.strip()


async def photo_cake(message):
    logger.debug(f'{photo_cake.__name__} - начало работы функции показывающей результаты поиска')
    response_list = SiteApiInterface(site_tg_settings.vk_login, 'Разрезы')
    global photos_links
    photos_links=response_list.get_photos()
    print(photos_links)
    await message.answer_photo(
        photo=photos_links[user_value],
        caption=f'photo 0',
        reply_markup=change_films_kb(num=0, all_num=len(photos_links)))
    return photos_links


async def update_num_text(message: Message, new_value: int):
    """Обновление описания картинки"""
    logger.debug(f'{update_num_text.__name__} - начало работы')
    global user_value
    user_value=new_value
    with suppress(TelegramBadRequest):
        photo = InputMediaPhoto(
            media=photos_links[new_value],
            caption=f'photo{new_value}')
        await message.edit_media(
            media=photo,
            reply_markup=change_films_kb(num=new_value, all_num=len(photos_links))
        )
    logger.info(f'{update_num_text.__name__} - КОнец работы')


async def callbacks_num(callback: CallbackQuery, state: FSMContext):
    """Кнопки колбэки"""
    logger.debug(f'{callbacks_num.__name__} - начало работы')
    # user_value = callback.from_user.id
    action = callback.data.split("_")[1]
    print(callback.message)
    print(user_value)
    print(action)
    # global user_value

    if action == "incr":
        # user_data[callback.from_user.id] = (user_value + 1) % len(dict_with_films[callback.from_user.id])
        await update_num_text(callback.message, (user_value + 1) % len(photos_links))
    elif action == "decr":
        # user_data[callback.from_user.id] = (user_value - 1) % len(dict_with_films[callback.from_user.id])
        await update_num_text(callback.message, (user_value - 1) % len(photos_links))
    await callback.answer(' ')
    # await state.set_state(new_state)
    # logger.info(f'{callbacks_num.__name__} - выполнил задачу')


if __name__ == '__main__':
    print('Nenm')
