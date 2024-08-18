import logging
import sys

from config_data.logger_config import *
import os.path

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from tg_api.utils.set_bot_commands import main_menu_commands

router = Router()

logger = logging.getLogger(f'main.tg_api.handlers.default_handlers.{os.path.basename(__file__)}')
sys.excepthook = any_exception


@router.message(Command('help'))
async def help_cmd(message: Message):
    """Кнопка помощи"""
    logger.debug(f'{help_cmd.__name__} - нажал кнопку помощи')
    text = ''
    if not message.from_user.username == 'BorisisTheBlade':
        text = [f'{el.command} - {el.description}' for el in main_menu_commands[:-1]]
    else:
        text = [f'{el.command} - {el.description}' for el in main_menu_commands]

    await message.answer(text='\n'.join(text), reply_markup=ReplyKeyboardRemove())
    logger.info(f'{help_cmd.__name__} - кнопка отработала')
