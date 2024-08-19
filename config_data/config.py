# Модуль получает токены бота из файла .env
import os
from dotenv import load_dotenv, find_dotenv


if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()


class SiteSettings:
    """Класс получения базовых настроек"""
    bot_key: str = os.getenv('BOT_TOKEN')
    bot_admin:str=os.getenv('ADMINISTRATOR')
    vk_token:str=os.getenv('VK_TOKEN')
    vk_login:str=os.getenv('VK_LOGIN')


site_tg_settings = SiteSettings()
if __name__ == '__main__':
    print(site_tg_settings.bot_key)
