from aiogram import Router
from aiogram.types import ReplyKeyboardRemove, Message
from requests import ReadTimeout

from database.core import def_insert_data
from database.models.models import Top100Films, db
from database.utilits.common_func import create_list_for_find_film
from site_api.core import def_top_100_film

router = Router()


@router.message()
async def rez_finder(message: Message):
    """Поиск фильмов по названию и вывод результата в виде картинки с описанием и кнопками листания"""
    try:
        # Top100Films.delete().execute()
        response_list = def_top_100_film()
        print(response_list)
        if isinstance(response_list, list) and len(response_list):
            out_list = create_list_for_find_film(None, response_list, None)
            def_insert_data(db, Top100Films, out_list)
        else:
            print(response_list)
    except ReadTimeout as exs:
        print(f'{exs} - сайт не отвечает')
