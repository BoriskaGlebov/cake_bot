import logging
from config_data.logger_config import *
import os.path
import sys

from aiogram import Router, Bot, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove
from tg_api.keyboards.reply.keybord_start import start_kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
# from database.core import def_insert_user
# from database.models.models import User
from tg_api.utils.set_bot_commands import set_main_menu_admin, set_main_menu

from config_data.config import site_tg_settings

logger = logging.getLogger(f'main.tg_api.handlers.custom_handlers.{os.path.basename(__file__)}')
sys.excepthook = any_exception

router = Router()


@router.message(Command('start'))
async def start_cmd(message: Message, bot: Bot, state: FSMContext):
    """Действия бота по команде start"""
    logger.debug('Пользователь нажал кнопку start')
    user = message.from_user
    if user.username == site_tg_settings.bot_admin:
        await set_main_menu_admin(bot)
    else:
        await set_main_menu(bot)
    me = await bot.get_me()
    await state.clear()
    await message.answer(f'Привет <b>{user.username}</b>!!!\n'
                         f'Меня зовут <b>{me.first_name}</b> и я могу отлично '
                         f'помочь с десертом.\n'
                         f'Дальше <b>нужно</b> выбрать какую то кнопку',
                         reply_markup=start_kb())

    await message.answer_sticker(
        sticker='CAACAgIAAxkBAAEMqzdmwh2TRAoOkqTa'
                'MnCOLcf36FoUjwACiwEAAiteUwujYbxpJDSDUDUE')
    await message.answer(text='Сюда можно добавить все что угодно')
    # def_insert_user(User, user.id, user.username)
    logger.info(f'{start_cmd.__name__} - отработала хорошо')


# Нетрудно догадаться, что следующие два хэндлера можно
# спокойно объединить в один, но для полноты картины оставим так

# default_state - это то же самое, что и StateFilter(None)
@router.message(StateFilter(default_state), Command(commands=["cancel"]))
@router.message(StateFilter(default_state), F.text.lower() == "отмена")
async def cmd_cancel_no_state(message: Message, state: FSMContext):
    """Сработает когда бот не FSM"""
    logger.debug(f'{cmd_cancel_no_state.__name__} - начало работы')
    await state.set_data({})
    await message.answer(
        text="Нечего отменять",
        reply_markup=ReplyKeyboardRemove()
    )
    logger.info(f'{cmd_cancel_no_state.__name__} - статус обнулен')


@router.message(Command(commands=["cancel"]), ~StateFilter(default_state))
@router.message(F.text.lower() == "отмена", ~StateFilter(default_state))
@router.message(F.text.lower() == "галя , у нас отмена", ~StateFilter(default_state))
async def cmd_cancel(message: Message, state: FSMContext):
    """Сработает если бот в FSM"""
    logger.debug(f'{cmd_cancel.__name__} - начало работы')
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=start_kb()
    )
    logger.info(f'{cmd_cancel.__name__} - статус обнулен')
