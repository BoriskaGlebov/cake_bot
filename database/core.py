# Модуль объединяет методы работы с БД
import logging

from database.utilits.CRUD import CRUDInterface

from database.models.models import *

def_insert_user = CRUDInterface.insert_single_user()
def_insert_data = CRUDInterface.insert_data()
def_get_elem = CRUDInterface.retrieve_elem()
def_del_old_elem = CRUDInterface.del_old_el()

# logger = logging.getLogger('main.database.' + str(os.path.relpath(__file__)))

if __name__ == '__main__':
    print('test')
    def_insert_user(User, 456789, 'BOriska')
    def_insert_user(User, 123, 'BOriska')
