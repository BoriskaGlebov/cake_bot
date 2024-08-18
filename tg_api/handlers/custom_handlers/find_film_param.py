import asyncio
import os.path
import sys

from config_data.logger_config import *
from aiogram import Router, F, Bot

from aiogram.filters import Command

from tg_api.states.user_state import MovieSearch
from tg_api.handlers.custom_handlers.common_func import *
from tg_api.keyboards.inline.some_inline_kb import change_films_kb
from tg_api.keyboards.inline.for_film_param import *

from site_api.core import def_find_film_param

from database.utilits.common_func import create_list_for_find_film
from database.models.models import User, Find_Film_Param, db
from database.core import def_insert_data, def_get_elem

import re

logger = logging.getLogger(f'main.tg_api.handlers.custom_handlers.{os.path.basename(__file__)}')
sys.excepthook = any_exception

router = Router()
genres = ['боевик', 'комедия', 'мультфильм', 'мелодрама', 'семейный', 'аниме',
          'биография', 'вестерн', 'военный', 'детектив', 'детский', 'для взрослых',
          'документальный', 'драма', 'игра', 'история', 'концерт', 'короткометражка', 'криминал',
          'музыка', 'мюзикл', 'новости', 'приключения', 'реальное ТВ',
          'спорт', 'ток-шоу', 'триллер', 'ужасы', 'фантастика', ' фильм-нуар', 'церемония', 'фэнтези']
countries = [el for el in countries_list()]


@router.message(F.text == 'Подбор 🎥 по параметрам')
@router.message(Command('find_param'))
async def finder_film(message: Message, state: FSMContext):
    """Действие по нажатии кнопки поиск фильмов, отображение новых кнопок"""
    logger.debug('Пользователь нажал кнопку поиска по параметрам')
    await message.answer('🤖 Сейчас будут предложены параметры поиска фильмов!', reply_markup=ReplyKeyboardRemove())
    await message.answer('Выберите, что будем искать?', reply_markup=film_type_kb())
    await state.set_state(MovieSearch.find_film_param)


@router.callback_query(MovieSearch.find_film_param, F.data.startswith('type'))
async def film_types(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """Выбор типа фильмов"""
    logger.debug(f'{film_types.__name__} - начало работы функции')
    user_value = callback.from_user.id
    action = callback.data.split('_')[1]
    if action == 'None':
        action = None
    user_data[user_value] = [action, 2019, 2024, 0, 10, 0]
    await callback.answer(f'{callback.from_user.username} выбрал {action}')
    logger.debug(f'{user_value},{user_data}]')
    await bot.send_message(chat_id=callback.message.chat.id, text='Спасибо, переходим к следующему параметру')
    await asyncio.sleep(1)
    await bot.send_message(chat_id=callback.message.chat.id, text='Теперь выбираем год\n от 2019 до 2024',
                           reply_markup=year_change_kb())
    await state.set_state(MovieSearch.choosing_year)
    logger.debug(f'{film_types.__name__} - конец работы функции')


@router.message(MovieSearch.find_film_param, F.text)
async def incorrect_type(message: Message):
    """Отработка некорректного запроса по типу фильмов"""
    await message.answer('Кажется вы не нажали на кнопку! Попробуйте еще раз!', reply_markup=film_type_kb())


async def edit_message_year(message: Message, value_l: int, value_r: int):
    """Изменение сообщения по вводу дат"""
    await message.edit_text(f'Теперь выбираем год\n от {value_l} до {value_r}', reply_markup=year_change_kb())


async def edit_message_rating(message: Message, value_l: int, value_r: int):
    """Изменение сообщения по вводу рейтинга"""
    await message.edit_text(f'Теперь введи нужный рейтинг?\n {value_l} - {value_r}', reply_markup=rating_change_kb())


async def edit_message_genres(message: Message, value: int):
    """Изменение сообщения по вводу жанра"""
    await message.edit_text(f'Теперь выбираем жанр?\n'
                            f'<b>{genres[value]}</b>', reply_markup=genres_change_kb())


@router.message(MovieSearch.choosing_year, F.text)
async def manual_year(message: Message, state: FSMContext):
    """Ручной ввод даты выхода фильмов"""
    user_value = message.from_user.id
    res = re.findall(r'\d{4}', message.text)
    logger.debug(f'{manual_year.__name__} - {res}')
    if len(res):
        if len(res) > 1 and int(res[0]) <= int(res[1]) <= 2024:
            user_data[message.from_user.id][1] = '-'.join(res[0:2])
        elif len(res) == 1 and int(res[0]) <= 2024:
            user_data[message.from_user.id][1] = '-'.join(res[0:1])
        else:
            await message.answer('Годы указаны неверно!\n Нужно в формате: 1874, 2050, !2020, 2020-2024')
            await message.answer('Теперь выбираем год\n от 2019 до 2024', reply_markup=year_change_kb())
            return
        del (user_data[message.from_user.id][2])
        logger.debug(f'{manual_year.__name__} - {user_data}')
        await message.answer(f"Итого: {user_data[user_value][1]}")
        await message.answer(text='Теперь введи нужный рейтинг?\n 0 - 10', reply_markup=rating_change_kb())
        await state.set_state(MovieSearch.choosing_rating)
    else:
        await message.reply('нажми кнопки', reply_markup=year_change_kb())


@router.callback_query(MovieSearch.choosing_year, F.data.startswith('year'))
async def year(callback: CallbackQuery, state: FSMContext):
    """Отработка выбора года фильмов"""
    user_value = callback.from_user.id
    action = callback.data.split('_')[1]
    logger.debug(f'{year.__name__} - {action}')
    # Значения прошлой итеррации
    value_l = user_data[user_value][1]
    value_r = user_data[user_value][2]
    if action == 'lplus':
        user_data[user_value][1] += 1
    elif action == 'lminus':
        user_data[user_value][1] -= 1
    elif action == 'rplus':
        user_data[user_value][2] += 1
    elif action == 'rminus':
        user_data[user_value][2] -= 1
    elif action == 'None':
        user_data[user_value][1] = None
        del (user_data[user_value][2])
        logger.debug(f'{year.__name__} - {user_data}')
        await callback.message.edit_text(f"Итого: Все равно")
        await callback.message.answer(text='Теперь введи нужный рейтинг?\n 0 - 10', reply_markup=rating_change_kb())
        await state.set_state(MovieSearch.choosing_rating)
        return
    elif action == 'finish':
        user_data[user_value][1] = '-'.join([str(user_data[user_value][1]), str(user_data[user_value][2])])
        del (user_data[user_value][2])
        logger.debug(f'{year.__name__} - {user_data}')
        await callback.message.edit_text(f"Итого: {user_data[user_value][1]}")
        await callback.message.answer(text='Теперь введи нужный рейтинг?\n 0 - 10', reply_markup=rating_change_kb())
        await state.set_state(MovieSearch.choosing_rating)
        return
    if user_data[user_value][1] <= user_data[user_value][2] < 2025 and user_data[user_value][2] < 2025:
        await edit_message_year(callback.message, user_data[user_value][1], user_data[user_value][2])
    else:
        user_data[user_value][1] = value_l
        user_data[user_value][2] = value_r
        await callback.answer('Не-а')
    logger.debug(f'{year.__name__} - {user_data}')


@router.message(MovieSearch.choosing_rating, F.text)
async def incorrect_rating(message: Message):
    """Обработка некорректного ввода рейтинга"""
    await message.answer('Лучше выбирать кнопками', reply_markup=rating_change_kb())


@router.callback_query(MovieSearch.choosing_rating, F.data.startswith('rating'))
async def rating_change(callback: CallbackQuery, state: FSMContext):
    """Выбираю рейтинги"""
    user_value = callback.from_user.id
    action = callback.data.split('_')[1]
    logger.debug(f'{rating_change.__name__} - {action}')
    # Значения прошлой итеррации
    value_l = user_data[user_value][2]
    value_r = user_data[user_value][3]
    if action == 'lplus':
        user_data[user_value][2] += 1
    elif action == 'lminus':
        user_data[user_value][2] -= 1
    elif action == 'rplus':
        user_data[user_value][3] += 1
    elif action == 'rminus':
        user_data[user_value][3] -= 1
    elif action == 'None':
        user_data[user_value][2] = None
        del (user_data[user_value][3])
        logger.debug(f'{rating_change.__name__} - {user_data}')
        await callback.message.edit_text(f"Итого: Все равно")
        await callback.message.answer(text=f'Теперь выбираем жанр?\n{genres[user_data[user_value][3]]}',
                                      reply_markup=genres_change_kb())
        await state.set_state(MovieSearch.choosing_genres)
        return
    elif action == 'finish':
        user_data[user_value][2] = '-'.join([str(user_data[user_value][2]), str(user_data[user_value][3])])
        del (user_data[user_value][3])
        logger.debug(f'{rating_change.__name__} - {user_data}')
        await callback.message.edit_text(f"Итого: {user_data[user_value][2]}")
        await callback.message.answer(text=f'Теперь выбираем жанр?\n{genres[user_data[user_value][3]]}',
                                      reply_markup=genres_change_kb())
        await state.set_state(MovieSearch.choosing_genres)
        return
    if 0 <= user_data[user_value][2] <= user_data[user_value][3] < 11 and user_data[user_value][3] < 11:
        await edit_message_rating(callback.message, user_data[user_value][2], user_data[user_value][3])
    else:
        user_data[user_value][2] = value_l
        user_data[user_value][3] = value_r
        await callback.answer('Не-а')
    logger.debug(f'{rating_change.__name__} - {user_data}')


@router.message(MovieSearch.choosing_genres, F.text)
async def incorrect_genres(message: Message):
    """Отработка некорректного ввода жанра"""
    await message.answer('Лучше выбирать жанр кнопками', reply_markup=genres_change_kb())


@router.callback_query(MovieSearch.choosing_genres, F.data.startswith('genres'))
async def genres_change(callback: CallbackQuery, state: FSMContext):
    """Выбираю жанры"""
    user_value = callback.from_user.id
    action = callback.data.split('_')[1]
    logger.debug(f'{genres_change.__name__} - {action}')
    # Значения прошлой итеррации
    value = user_data[user_value][3]
    if action == 'left':
        user_data[user_value][3] -= 1
    elif action == 'right':
        user_data[user_value][3] += 1
    elif action == 'None':
        user_data[user_value][3] = None
        logger.debug(f'{genres_change.__name__} - {user_data}')
        await callback.message.edit_text(f"Итого: Все равно")
        await callback.message.answer(text='Теперь введи название страны?')
        await callback.message.answer(text='Введите название страны', reply_markup=countries_kb())
        await state.set_state(MovieSearch.choosing_country)
        return
    elif action == 'finish':
        user_data[user_value][3] = genres[user_data[user_value][3]]
        logger.debug(f'{genres_change.__name__} - {user_data}')
        await callback.message.edit_text(f"Итого: {user_data[user_value][3]}")
        await callback.message.answer(text='Теперь введи название страны?')
        await callback.message.answer(text='Введите название страны', reply_markup=countries_kb())
        await state.set_state(MovieSearch.choosing_country)
        return
    if -1 < user_data[user_value][3] <= len(genres):
        await edit_message_genres(callback.message, user_data[user_value][3])
    else:
        user_data[user_value][3] = value
        await callback.answer('Не-а')
    logger.debug(f'{genres_change.__name__} - {user_data}')


@router.callback_query(MovieSearch.choosing_country, F.data.startswith('countries'))
async def countries_choice_callback(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """ОБработка колбэков по странм если кнопка None"""
    print(callback.data)
    user_inf = callback.from_user.id
    action = callback.data.split('_')[1]
    user_data[user_inf].append(None)
    logger.debug(f'{countries_choice_callback.__name__} - {user_data}')
    def_del_old_elem(db, user_inf, Find_Film_Param, User)
    await bot.send_message(chat_id=callback.message.chat.id, text='Вот все выбрали!')
    await bot.send_message(chat_id=callback.message.chat.id, text='Тип = {0}\n'
                                                                  'Год = {1}\n'
                                                                  'Рейтинг = {2}\n'
                                                                  'Жанр = {3}\n'
                                                                  'Страна= {4}\n'
                           .format(*[el if el is not None else 'Все равно' for el in user_data[user_inf]]))
    try:
        response_list = def_find_film_param(*user_data[user_inf])
        if isinstance(response_list, list) and len(response_list):
            out_list = create_list_for_find_film(User.get(User.user_id == user_inf), response_list,
                                                 ','.join(
                                                     [el if el is not None else 'Все равно'
                                                      for el in user_data[user_inf]]))
            def_insert_data(db, Find_Film_Param, out_list)
            if user_inf in dict_with_films:
                del dict_with_films[user_inf]
            if user_inf in user_data:
                del user_data[user_inf]

            dict_with_films[user_inf] = def_get_elem(db, user_inf, Find_Film_Param, User)
            await bot.send_photo(chat_id=callback.message.chat.id,
                                 photo=photo_finder(num=0, user_id=user_inf, out_message_dict=dict_with_films),
                                 caption=caption(num=0, user_id=user_inf, out_message_dict=dict_with_films),
                                 reply_markup=change_films_kb(num=0, all_num=len(dict_with_films[user_inf])))
            await state.set_state(MovieSearch.changing_films_find_film_param)
        elif isinstance(response_list, list):
            await bot.send_message(callback.message.chat.id, text='А я не знаю такой фильм 🤖')
        else:
            logger.debug(f'{countries_choice_callback.__name__} - {response_list}')
            await bot.send_message(callback.message.chat.id, text='Что то пошло не так ! Буду разбираться',
                                   reply_markup=ReplyKeyboardRemove())
            await bot.send_sticker(callback.message.chat.id,
                                   sticker='CAACAgIAAxkBAAELUIxlv4FmGKw0Z7rVlCfWSo1gTA_n1wACWQADJxRJC-OPDSX1raG1NAQ')
            await state.clear()
    except ReadTimeout as exs:
        logger.exception('сайт не отвечает', exc_info=True)
        await bot.send_message(callback.message.chat.id, text='Упсссс...Сервер не отвечает',
                               reply_markup=ReplyKeyboardRemove())
        await bot.send_message(callback.message.chat.id,
                               text='CAACAgIAAxkBAAELUIxlv4FmGKw0Z7rVlCfWSo1gTA_n1wACWQADJxRJC-OPDSX1raG1NAQ')
    await state.set_state(MovieSearch.changing_films_find_film_param)


@router.message(MovieSearch.choosing_country, F.text.title().in_(countries))
async def countries_choice(message: Message, state: FSMContext):
    """Обработка ввода страны"""
    user_value = message.from_user.id
    if message.text.upper() in ['США', 'СССР', 'ЦАР', 'ОАЭ']:
        user_data[user_value].append(message.text.upper())
    else:
        user_data[user_value].append(message.text.title())
    await message.answer('Вот все и выбрали!')
    await message.answer(text='Тип = {0}\n'
                              'Год = {1}\n'
                              'Рейтинг = {2}\n'
                              'Жанр = {3}\n'
                              'Страна= {4}\n'.format(*[el if el is not None else 'Все равно'
                                                       for el in user_data[user_value]]))
    logger.debug(f'{countries_choice.__name__} - {user_data}')
    await state.set_state(MovieSearch.choosing_find_film_param)
    await rez_finder(message, state, MovieSearch.changing_films_find_film_param, Find_Film_Param)


@router.message(MovieSearch.choosing_country, F.text)
async def incorrect_country(message: Message):
    """Обработка некорректной страны"""
    await message.answer('Такой страны нету!', reply_markup=countries_kb())


@router.callback_query(MovieSearch.changing_films_find_film_param, F.data.startswith("num_"))
async def callbacks_films(callback: CallbackQuery, state: FSMContext):
    await callbacks_num(callback, state, MovieSearch.changing_films_find_film_param)
