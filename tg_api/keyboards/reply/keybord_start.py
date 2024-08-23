from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def start_kb(buttons: list) -> ReplyKeyboardMarkup:
    """Rеply кнопки основных функций бота"""
    builder = ReplyKeyboardBuilder()
    but = [KeyboardButton(text=b) for b in buttons]
    for num in range(0, len(but) + 1, 2):
        builder.row(*but[num:num + 2])
    return builder.as_markup(resize_keyboard=True)
