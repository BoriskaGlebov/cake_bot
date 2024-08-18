import unittest
from site_api.utils.site_api_func import SiteApiInterface
import logging

# отключаю логгирование на момент тестов
logger = logging.getLogger(__name__)
logging.disable(level=40)  # level = ERROR


class SiteApiInterfaceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.film_finder = SiteApiInterface.film_finder()
        cls.top_100 = SiteApiInterface.top_100_film()
        cls.film_param = SiteApiInterface.find_film_param()
        cls.films = ['1+1', 'Терминатор', 'Троя']
        cls.params_correct = [['movie', '2018-2024', '7-10', 'боевик', 'Россия'],
                              ['cartoon', '2016', '7-10', None, 'США'],
                              ['anime', '2007-2018', '7-10', None, 'Россия']
                              ]
        cls.params_uncorrect = [['mov', '2018-2024', '7-10', 'боевик', 'Россия'],
                                ['cartoon', 'sdfhjhk', '7-10', None, 'США'],
                                ['anime', '2007-2018', 'asd', None, 'adlad;a']
                                ]

    def test_correct_find_film(self):
        for i in SiteApiInterfaceTest.films:
            with self.subTest('Под тест'):
                res = SiteApiInterfaceTest.film_finder(i)
                self.assertIsInstance(res, list)

    def test_uncorrect_find_film(self):
        res = SiteApiInterfaceTest.film_finder('adfnlaflaf;ff')
        size = len(res)
        self.assertEqual(size, 0)

    def test_correct_top100_film(self):
        res = SiteApiInterfaceTest.top_100()
        self.assertIsInstance(res, list)

    def test_correct_find_film_param(self):
        for i in SiteApiInterfaceTest.params_correct:
            with self.subTest('Под тест'):
                res = SiteApiInterfaceTest.film_param(*i)
                self.assertIsInstance(res, list)

    def test_uncorrect_find_film_param(self):
        for i in SiteApiInterfaceTest.params_uncorrect:
            with self.subTest('Под тест'):
                res = SiteApiInterfaceTest.film_param(*i)
                self.assertEqual(res, 400)
