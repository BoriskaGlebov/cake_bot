import logging
import os
import sys

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from config_data.logger_config import any_exception
from database.models.models import User

from database.models.models import FilmsBase, Find_Film_Param

logger = logging.getLogger(f'main.tg_api.handlers.custom_handlers.{os.path.basename(__file__)}')
sys.excepthook = any_exception

router = Router()


@router.message(F.text == '📜История запросов')
@router.message(Command('history'))
async def history(message: Message):
    """Итория запросов по Боту"""
    logger.debug(f'{history.__name__} - начало работы')
    await message.answer('Здесь покажу историю запросов по поиску фильмов')
    value = FilmsBase.select(FilmsBase.query).join(User).where(User.user_id == message.from_user.id)
    out_res = set(el.query for el in value)
    if len(out_res):
        await message.answer(text='\n'.join(out_res))
    else:
        await message.answer('А вы еще не искали фильмы')
    await message.answer('Здесь покажу историю запросов по поиску фильмов c параметрами')
    value2 = Find_Film_Param.select(Find_Film_Param.query).join(User).where(User.user_id == message.from_user.id)
    out_res2 = set(el.query for el in value2)
    if len(out_res2):
        for el in out_res2:
            await message.answer(text='Тип = {0}\n'
                                      'Год = {1}\n'
                                      'Рейтинг = {2}\n'
                                      'Жанр = {3}\n'
                                      'Страна= {4}\n'
                                 .format(*el.split(',')))
    else:
        await message.answer('А вы еще не искали фильмы по параметрам')
    logger.info(f'{history.__name__} - отработала хорошо')
