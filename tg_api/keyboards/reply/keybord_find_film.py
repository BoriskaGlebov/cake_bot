from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import KeyboardButton, ReplyKeyboardBuilder


def get_bot_function_find_film() -> ReplyKeyboardMarkup:
    """Кнопка Поиск 🎥 по названию"""
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="Поиск 🎥 по названию"),
                KeyboardButton(text="Галя , у нас ОТМЕНА"))
    return builder.as_markup(resize_keyboard=True, input_field_placeholder='Введи название фильма?')
