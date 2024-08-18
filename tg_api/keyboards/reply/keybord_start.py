from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def start_kb() -> ReplyKeyboardMarkup:
    """Rеply кнопки основных функций бота"""
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text='Поиск 🎥 по названию'),
                KeyboardButton(text='Подбор 🎥 по параметрам'))
    builder.row(KeyboardButton(text='Топ 100 🎥 Кинопоиска'),
                KeyboardButton(text='📜История запросов'))
    return builder.as_markup(resize_keyboard=True)
