from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


def change_films_kb(num, all_num) -> InlineKeyboardMarkup:
    """Инлайн кнопки прокрутки результата"""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="👈", callback_data="num_decr"),
                InlineKeyboardButton(text=f'{num + 1}/{all_num}', callback_data='num_page'),
                InlineKeyboardButton(text="👉", callback_data="num_incr"))
    return builder.as_markup()
