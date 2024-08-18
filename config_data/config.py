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


site_tg_settings = SiteSettings()
if __name__ == '__main__':
    print(site_tg_settings.bot_key)