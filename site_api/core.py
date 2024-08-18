# Модуль собирает все данные для работы с api kinopoisk
import logging
import os.path
from logging import config
from config_data.logger_config import dict_config

from site_api.utils.site_api_func import SiteApiInterface

def_find_film = SiteApiInterface.film_finder()
def_top_100_film = SiteApiInterface.top_100_film()
def_find_film_param = SiteApiInterface.find_film_param()

# logger = logging.getLogger('main.site_api.' + str(os.path.relpath(__file__)))

if __name__ == '__main__':
    pass
