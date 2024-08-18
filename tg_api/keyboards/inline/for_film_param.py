from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


def film_type_kb() -> InlineKeyboardMarkup:
    """Инлайн кнопки выбора типа фильмов"""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='🎬Фильм', callback_data='type_movie'),
                InlineKeyboardButton(text='🎬Сериал', callback_data='type_tv-series'))
    builder.row(InlineKeyboardButton(text='🐨Мультик', callback_data='type_cartoon'))
    builder.row(InlineKeyboardButton(text='🥷Аниме-сериал', callback_data='type_animated-series'),
                InlineKeyboardButton(text='🥷Аниме', callback_data='type_anime'))
    builder.row(InlineKeyboardButton(text='Все равно', callback_data='type_None'))
    return builder.as_markup()


def year_change_kb() -> InlineKeyboardMarkup:
    """Выбор года"""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='-', callback_data='year_lminus'),
                InlineKeyboardButton(text='+', callback_data='year_lplus'),
                InlineKeyboardButton(text='-', callback_data='year_rminus'),
                InlineKeyboardButton(text='+', callback_data='year_rplus'))
    builder.row(InlineKeyboardButton(text='🆗', callback_data='year_finish'))
    builder.row(InlineKeyboardButton(text='Все равно', callback_data='year_None'))
    return builder.as_markup()


def rating_change_kb() -> InlineKeyboardMarkup:
    """Выбор рейтинга"""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='-', callback_data='rating_lminus'),
                InlineKeyboardButton(text='+', callback_data='rating_lplus'),
                InlineKeyboardButton(text='-', callback_data='rating_rminus'),
                InlineKeyboardButton(text='+', callback_data='rating_rplus'))
    builder.row(InlineKeyboardButton(text='🆗', callback_data='rating_finish'))
    builder.row(InlineKeyboardButton(text='Все равно', callback_data='rating_None'))
    return builder.as_markup()


def genres_change_kb() -> InlineKeyboardMarkup:
    """Выбор жанра"""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='👈', callback_data='genres_left'),
                InlineKeyboardButton(text='👉', callback_data='genres_right'))
    builder.row(InlineKeyboardButton(text='🆗', callback_data='genres_finish'))
    builder.row(InlineKeyboardButton(text='Все равно', callback_data='genres_None'))
    return builder.as_markup()


def countries_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='Все равно!', callback_data='countries_None'))
    return builder.as_markup()
