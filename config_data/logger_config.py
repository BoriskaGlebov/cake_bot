# Словарь настройки логирования проекта
import logging
import os
from logging import config
from logging import FileHandler
from logging.handlers import TimedRotatingFileHandler
import sys
import string

default_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


def any_exception(type, values, traceback_info):
    """
    Функция логирования неожиданных исключений
    """
    logger = logging.getLogger('main')
    logging.config.dictConfig(dict_config)
    logger.error(f'some error {type} {values} {traceback_info}', exc_info=(type, values, traceback_info))


dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
            "format": "%(asctime)s | %(levelname)s | %(name)s | line %(lineno)d | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "base"

        },
        "file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "base",
            "filename": f'{default_path}/logger.log',
            "mode": "a",
            "encoding": "utf-8",
        },

    },
    "loggers": {
        "main": {
            "level": "DEBUG",
            "handlers": ["file", "console"],
        },

    },
    # "filters": {
    #     "my_filter": {
    #         "()": SelfFilter,
    #     }
    # },
    # "root":{},
}
