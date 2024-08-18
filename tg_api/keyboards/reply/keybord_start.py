from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def start_kb() -> ReplyKeyboardMarkup:
    """Rеply кнопки основных функций бота"""
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text='Подбор 1 товара'),
                KeyboardButton(text='Подбор 1 товара'))
    builder.row(KeyboardButton(text='Подбор 1 товара 🎥 '),
                KeyboardButton(text='📜История запросов'))
    return builder.as_markup(resize_keyboard=True)
