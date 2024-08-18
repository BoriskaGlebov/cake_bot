# модуль необходим в начале проекта для создания колонок в БД
from typing import Callable
from functools import wraps


def column_names(func: Callable) -> Callable:
    """Возвращает название ключей в словаре, для заполнения названий колонок в таблице"""

    @wraps(func)
    def wrap_func(*args, **kwargs):
        # Для получения заголовков словаря и типов данных в них
        some_res = func(*args, **kwargs)
        with open('test.txt', 'w', encoding='UTF8') as file:
            for key, val in some_res[0].items():
                if isinstance(val, int):
                    file.write(f'{key} = peewee.IntegerField(null=True)\n')
                elif isinstance(val, str) or val is None:
                    file.write(f'{key} = peewee.TextField(null=True)\n')
                elif isinstance(val, bool):
                    file.write(f'{key} = peewee.BooleanField()\n')
                else:
                    file.write(f'{key} = JSONField(null=True, json_dumps=my_json_dumps)\n')
            file.write(f'Всего элементов = {str(len(some_res[0]))}')

        return some_res

    return wrap_func
