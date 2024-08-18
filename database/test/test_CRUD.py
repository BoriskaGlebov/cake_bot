import unittest
from database.utilits.CRUD import CRUDInterface
from database.utilits.common_func import create_list_for_find_film
from site_api.core import *
from database.models.models import *
from database.utilits.common_func import create_list_for_find_film

logger = logging.getLogger(__name__)


logging.disable(level=40)  # level = ERROR


class Test_CRUDInterface(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.single_user_correct: tuple = (User, 123456, 'Some Test User')

    def test_correct_insert_single_user(self):
        single_user = CRUDInterface.insert_single_user()
        res = single_user(*self.single_user_correct)
        resp_db = User.select(User.user_id, User.user_name).where(
            User.user_id == self.single_user_correct[1]).tuples()
        self.assertEqual(Test_CRUDInterface.single_user_correct[1:], resp_db[0])

    def test_single_insert_single_user(self):
        single_user = CRUDInterface.insert_single_user()
        res = single_user(*self.single_user_correct)
        resp_db = User.select(User.user_id, User.user_name).where(
            User.user_id == self.single_user_correct[1]).tuples().__len__()
        self.assertEqual(resp_db, 1)

    def test_insert_data(self):
        find_film = def_find_film('1+1')
        user = User.select().where(User.user_id == self.single_user_correct[1])[0]
        cor_res = create_list_for_find_film(user, find_film, '1+1')
        insert_data = CRUDInterface.insert_data()
        from_db = insert_data(db, FilmsBase, cor_res)
        res_from_db = FilmsBase.select().where(user)
        self.assertEqual(len(cor_res), len(res_from_db))

    def test_retrieve_elem(self):
        user = User.select().where(User.user_id == self.single_user_correct[1])
        init = CRUDInterface.retrieve_elem()
        data_db = init(db, int(user[0].user_id), FilmsBase, User)
        self.assertTrue(data_db.__len__() > 0)

    def test_del_inst(self):
        user = User.select().where(User.user_id == self.single_user_correct[1])
        print(user)
        func = CRUDInterface.del_old_el()
        res = func(db, 123456, FilmsBase, User)
        self.assertEqual(len(res),0)


    #
    # func = CRUDInterface.del_old_el()
    # res_for_del = func(db, user[0], FilmsBase, User)
    # print(len(res_for_del))
    # # print(user[0])
    # some = res_from_db(db, user[0].user_id, FilmsBase, User)
    # print(len(some))

    @classmethod
    def tearDownClass(cls):
        User.select().where(User.user_id == cls.single_user_correct[1])[0].delete_instance(recursive=True)
