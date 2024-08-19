# Модуль основных функций с сайта Kinopoisk
import logging
import os.path
import sys
from pprint import pprint

from config_data.logger_config import dict_config, any_exception
from config_data.config import site_tg_settings
import requests

# from site_api.settings.site_settings import headers_dict, status_code
# from site_api.utils.common_func import column_names

logger = logging.getLogger(f'main.site_api.utils.{os.path.basename(__file__)}')
sys.excepthook = any_exception
# logging.config.dictConfig(dict_config)  # это на период тестирования



class SiteApiInterface:
    """
    Интерфейс поиска картинок тортиков
    """

    @classmethod
    def get_id_contact(cls, id_name: str) -> int:
        """
        Получает id пользователя
        :param id_name: ID как в заголовке на сайте ВК
        :return: ID как в нужно в API
        """
        method = 'users.get'
        params = {'user_ids': id_name,
                  'access_token': site_tg_settings.vk_token,
                  'v': '5.199 HTTP/1.1'
                  }
        query = requests.get(url=f'https://api.vk.com/method/{method}', params=params)
        if query.status_code == 200:
            return query.json().get('response')[0].get('id')

    @classmethod
    def get_user_albums(cls, user_id: int, album_name: str):
        """
        Получает ID нужного альбома по его названию
        :param user_id: ID как в API
        :param album_name: Название альбома как на сайте
        :return: ID нужного альбома
        """
        method = 'photos.getAlbums'
        params = {'owner_id': str(user_id),
                  'access_token': site_tg_settings.vk_token,
                  'v': '5.199 HTTP/1.1'
                  }
        query = requests.get(url=f'https://api.vk.com/method/{method}', params=params)
        if query.status_code == 200:
            albums = query.json().get('response').get('items')
            for album in albums:
                if album.get('title') == album_name:
                    return album.get('id')

    @classmethod
    def get_photos(cls, owner_id: int, album_id: int) -> list:
        """
        Получаю ссылки на фото в альбоме
        :param owner_id: ID Пользователя
        :param album_id: ID альбома
        :return: список ссылок на оригинал фото
        """
        method = 'photos.get'
        params = {'owner_id': owner_id,
                  'album_id': album_id,
                  'access_token': site_tg_settings.vk_token,
                  'v': '5.199 HTTP/1.1'
                  }
        query = requests.get(url=f'https://api.vk.com/method/{method}', params=params)
        if query.status_code == 200:
            photos = query.json().get('response').get('items')
            photo_url = [photo.get('orig_photo').get('url') for photo in photos]
            return photo_url


if __name__ == '__main__':
    user_id = SiteApiInterface.get_id_contact(site_tg_settings.vk_login)
    print(user_id)
    user_albums = SiteApiInterface.get_user_albums(user_id, 'Разрезы')
    print(user_albums)
    album_photo = SiteApiInterface.get_photos(user_id, user_albums)
    print(album_photo)
