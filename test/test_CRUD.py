import os.path
import unittest
from unittest import TestCase

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from database.utilits.CRUD import CRUDInterface
from database.models.models import User,session,Base
import logging

logger = logging.getLogger(__name__)
logging.disable(level=40)  # level = ERROR

default_path = os.path.dirname(__file__)


class Test_CRUDInterface(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine(f'sqlite:///{default_path}/test_cake_base.db')
        cls.Session = sessionmaker(bind=cls.engine)
        cls.session = cls.Session()
        Base.metadata.create_all(cls.engine)
        cls.correct_user={'session':cls.session,'user_name':'Test_name','user_id':1234567890,}



    def test_correct_insert_single_user(self):
        single_user = CRUDInterface.insert_single_user(**self.correct_user)
        test_user=self.session.query(User).where(User.user_id==single_user.user_id).all()[-1]
        self.assertEqual(single_user,test_user)



    @classmethod
    def tearDownClass(cls):
        cls.session.close()
        if os.path.isfile(f'{default_path}/test_cake_base.db'):
            os.remove(f'{default_path}/test_cake_base.db')
