from aiogram import Router, F
from aiogram.filters import Command
import logging

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from config_data.logger_config import any_exception, dict_config
from config_data.config import site_tg_settings
import os
import sys

# from tg_api.keyboards.reply.keybord_find_film import get_bot_function_find_film
from tg_api.handlers.custom_handlers.common_func2 import photo_cake,callbacks_num
from tg_api.states.user_state import OrderState

from site_api.site_api_func import SiteApiInterface

logger = logging.getLogger(f'main.tg_api.handlers.custom_handlers.{os.path.basename(__file__)}')
sys.excepthook = any_exception
router = Router()


@router.message(F.text == 'Кейк попс')
@router.message(Command('cake_pops'))
async def cake_pops(message: Message, state: FSMContext):
    """Действие по нажатии кнопки cake pops"""
    logger.debug(f'{cake_pops.__name__} - начало работы')
    await message.answer('Вы выбрали кейк попс и сейчас я покажу какие варианты можно будет заказать',
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(OrderState.cake_pops_photo)
    await message.answer('Отправиь любой текст что б продолжить')
    logger.info(f'{cake_pops.__name__} - отработало хорошо')


@router.message(OrderState.cake_pops_photo, F.text)
async def cake_pops_photo(message: Message, state: FSMContext):
    """Показываю фото кей попсов"""
    r = await state.get_state()
    await message.answer(r)
    await  message.answer('Здесь должны появиться фото кейк попсов')
    d = await photo_cake(message)
    print(message.text)

#
@router.callback_query(OrderState.cake_pops_photo, F.data.startswith("num_"))
async def callbacks_photos(callback: CallbackQuery, state: FSMContext):
    """Работа кнопок"""
    await callbacks_num(callback, state)
#
#
# @router.message(MovieSearch.changing_films, F.text)
# async def change_state(message: Message, state: FSMContext):
#     """Поиск фильма без команды поиска"""
#     await state.set_state(MovieSearch.choosing_film_name)
#     r = await state.get_state()
#     await rez_finder(message, state, MovieSearch.changing_films, FilmsBase)
