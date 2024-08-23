import unittest

from config_data.config import site_tg_settings
from site_api.site_api_func import SiteApiInterface
import logging

# отключаю логгирование на момент тестов
logger = logging.getLogger(__name__)
logging.disable(level=40)  # level = ERROR


class SiteApiInterfaceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.irina = SiteApiInterface(site_tg_settings.vk_login, "Разрезы")

    def test_get_id_contact(self):
        self.assertEqual(self.irina.get_id_contact(), 710973867)

    def test_get_user_albums(self):
        self.assertEqual(self.irina.get_user_albums(), 281795059)

    def test_get_photos(self):
        photo = self.irina.get_photos()
        self.assertIsInstance(photo, list)
