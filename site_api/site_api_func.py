# Модуль основных функций с сайта Kinopoisk
import logging
import logging.config
import os.path
import sys
from pprint import pprint

from config_data.logger_config import dict_config, any_exception
from config_data.config import site_tg_settings
import requests

# from site_api.settings.site_settings import headers_dict, status_code
# from site_api.utils.common_func import column_names

logger = logging.getLogger(f'main.site_api.{os.path.basename(__file__)}')
sys.excepthook = any_exception
logging.config.dictConfig(dict_config)  # необходимо на момент разработки, после надо убрать


class SiteApiInterface:
    """
    Интерфейс поиска картинок тортиков
    """

    def __init__(self, user_login: int, album_name: str | None = None):
        self.user_login = user_login
        self.album_name = album_name
        self.user_id = self.get_id_contact()
        logger.debug(f'{self.__class__.__name__} - Объект инициирован успешно')

    def get_id_contact(self) -> int:
        """
        Получает id пользователя
        :return: ID как в нужно в API
        """
        method = 'users.get'
        params = {'user_ids': self.user_login,
                  'access_token': site_tg_settings.vk_token,
                  'v': '5.199 HTTP/1.1'
                  }
        logger.debug(f'{self.get_id_contact.__name__} - Запроc на сервер VK')
        query = requests.get(url=f'https://api.vk.com/method/{method}', params=params)
        if query.status_code == 200:
            logger.debug(f'{self.get_id_contact.__name__} - Получил корректный ответ от сервера')
            return query.json().get('response')[0].get('id')
        logger.warning(f'{self.get_id_contact.__name__} - Не получил корректный ответ от сервера')

    def get_user_albums(self):
        """
        Получает ID нужного альбома по его названию
        :return: ID нужного альбома
        """
        method = 'photos.getAlbums'
        params = {'owner_id': self.user_id,
                  'access_token': site_tg_settings.vk_token,
                  'v': '5.199 HTTP/1.1'
                  }
        logger.debug(f'{self.get_user_albums.__name__} - Запроc на сервер VK')
        query = requests.get(url=f'https://api.vk.com/method/{method}', params=params)
        if query.status_code == 200:
            logger.debug(f'{self.get_user_albums.__name__} - Получил корректный ответ от сервера')
            albums = query.json().get('response').get('items')
            for album in albums:
                if album.get('title') == self.album_name:
                    return album.get('id')
        logger.warning(f'{self.get_user_albums.__name__} - Не получил корректный ответ от сервера')

    def get_photos(self) -> list:
        """
        Получаю ссылки на фото в альбоме
        :return: список ссылок на оригинал фото
        """
        method = 'photos.get'
        params = {'owner_id': self.user_id,
                  'album_id': self.get_user_albums(),
                  'access_token': site_tg_settings.vk_token,
                  'v': '5.199 HTTP/1.1'
                  }
        logger.debug(f'{self.get_photos.__name__}Запроc на сервер VK')
        query = requests.get(url=f'https://api.vk.com/method/{method}', params=params)
        if query.status_code == 200:
            logger.debug(f'{self.get_photos.__name__} - Получил корректный ответ от сервера')
            photos = query.json().get('response').get('items')
            photo_url = [photo.get('orig_photo').get('url') for photo in photos]
            return photo_url
        logger.warning(f'{self.get_photos.__name__} - Не получил корректный ответ от сервера')


#

if __name__ == '__main__':
    irina = SiteApiInterface(site_tg_settings.vk_login, "Разрезы")
    print(irina.get_id_contact())
    print(irina.get_user_albums())
    print(irina.get_photos())
