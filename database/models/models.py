# Модуль описывает таблицы БД
import logging
import logging.config
import os
import sys
from datetime import datetime
from http.cookiejar import Cookie
from os.path import pardir
from tkinter.font import names

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.dialects.sqlite import DATETIME
from sqlalchemy.orm import sessionmaker, declarative_base
from config_data.logger_config import any_exception, dict_config, default_path

logger = logging.getLogger(f'main.database.models.{os.path.basename(__file__)}')
sys.excepthook = any_exception
logging.config.dictConfig(dict_config)  # необходимо на момент разработки, после надо убрать


def correct_date():
    """
    Функция определяет корректное время добавляемое в таблицы БД по умолчанию
    :return: корректное дата, время
    """
    res = datetime.now().strftime('%Y-%m-%d %X')
    return res


engine = create_engine(f'sqlite:///{default_path}/cake_base.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class User(Base):
    """Таблица с пользователями бота"""
    __tablename__ = 'user'
    id: Column = Column(Integer, primary_key=True)
    user_id: Column = Column(Integer, nullable=False, default=123,unique=True)
    name: Column = Column(String, nullable=False, default='some_user')
    data: Column = Column(DATETIME, nullable=False, default=datetime.now)

    def __repr__(self) -> str:
        return ' | '.join([str(getattr(self, el.name)) for el in self.__table__.columns])


# default_path = os.path.dirname(os.path.abspath(__file__)).split('bot')[0] + 'bot/app'
# db_path = os.path.join(default_path, 'films.db')
# db = peewee.SqliteDatabase(db_path, 'film.db')
# # Для отключения экранирования в таблицах
# my_json_dumps = functools.partial(json.dumps, ensure_ascii=False)

#
#
# class ModelBase(peewee.Model):
#     """Модель базы данных"""
#     created_at = peewee.DateTimeField(default=correct_date)
#
#     class Meta:
#         database = db
#
#
# class User(ModelBase):
#     """Модель таблицы с пользователями"""
#     user_id = peewee.IntegerField()
#     user_name = peewee.TextField(null=True)
#
#
# class FilmsBase(ModelBase):
#     """Таблица для запроса поиска фильмов по названию"""
#     user = peewee.ForeignKeyField(User, backref='query')
#     query = peewee.TextField()
#     film_id = peewee.IntegerField(null=True)
#     internalNames = JSONField(null=True, json_dumps=my_json_dumps)
#     name = peewee.TextField(null=True)
#     alternativeName = peewee.TextField(null=True)
#     enName = peewee.TextField(null=True)
#     year = peewee.IntegerField(null=True)
#     genres = JSONField(null=True, json_dumps=my_json_dumps)
#     countries = JSONField(null=True, json_dumps=my_json_dumps)
#     releaseYears = JSONField(null=True, json_dumps=my_json_dumps)
#     externalId = JSONField(null=True, json_dumps=my_json_dumps)
#     names = JSONField(null=True, json_dumps=my_json_dumps)
#     type = peewee.TextField(null=True)
#     description = peewee.TextField(null=True)
#     shortDescription = peewee.TextField(null=True)
#     logo = JSONField(null=True, json_dumps=my_json_dumps)
#     poster = JSONField(null=True, json_dumps=my_json_dumps)
#     backdrop = JSONField(null=True, json_dumps=my_json_dumps)
#     rating = JSONField(null=True, json_dumps=my_json_dumps)
#     votes = JSONField(null=True, json_dumps=my_json_dumps)
#     movieLength = peewee.IntegerField(null=True)
#     isSeries = peewee.IntegerField(null=True)
#     ticketsOnSale = peewee.IntegerField(null=True)
#     totalSeriesLength = peewee.TextField(null=True)
#     seriesLength = peewee.TextField(null=True)
#     ratingMpaa = peewee.TextField(null=True)
#     ageRating = peewee.TextField(null=True)
#     top10 = peewee.TextField(null=True)
#     top250 = peewee.TextField(null=True)
#     typeNumber = peewee.IntegerField(null=True)
#     status = peewee.TextField(null=True)
#     internalRating = JSONField(null=True, json_dumps=my_json_dumps)
#     internalVotes = peewee.IntegerField(null=True)
#
#
# class Top100Films(ModelBase):
#     """Таблица для хранения топ 100 фильмов Кинопоиска"""
#     film_id = peewee.IntegerField(null=True)
#     name = peewee.TextField(null=True)
#     alternativeName = peewee.TextField(null=True)
#     rating = JSONField(null=True, json_dumps=my_json_dumps)
#     movieLength = peewee.IntegerField(null=True)
#     description = peewee.TextField(null=True)
#     year = peewee.IntegerField(null=True)
#     poster = JSONField(null=True, json_dumps=my_json_dumps)
#     genres = JSONField(null=True, json_dumps=my_json_dumps)
#     networks = peewee.TextField(null=True)
#     videos = JSONField(null=True, json_dumps=my_json_dumps)
#
#
# class Find_Film_Param(ModelBase):
#     """Таблица найденных фильмов по параметрам"""
#     user = peewee.ForeignKeyField(User, backref='query')
#     query = peewee.TextField()
#     film_id = peewee.IntegerField(null=True)
#     name = peewee.TextField(null=True)
#     status = peewee.TextField(null=True)
#     externalId = JSONField(null=True, json_dumps=my_json_dumps)
#     rating = JSONField(null=True, json_dumps=my_json_dumps)
#     votes = JSONField(null=True, json_dumps=my_json_dumps)
#     backdrop = JSONField(null=True, json_dumps=my_json_dumps)
#     images = JSONField(null=True, json_dumps=my_json_dumps)
#     productionCompanies = JSONField(null=True, json_dumps=my_json_dumps)
#     spokenLanguages = JSONField(null=True, json_dumps=my_json_dumps)
#     type = peewee.TextField(null=True)
#     description = peewee.TextField(null=True)
#     distributors = JSONField(null=True, json_dumps=my_json_dumps)
#     premiere = JSONField(null=True, json_dumps=my_json_dumps)
#     slogan = peewee.TextField(null=True)
#     year = peewee.IntegerField(null=True)
#     poster = JSONField(null=True, json_dumps=my_json_dumps)
#     facts = JSONField(null=True, json_dumps=my_json_dumps)
#     genres = JSONField(null=True, json_dumps=my_json_dumps)
#     countries = JSONField(null=True, json_dumps=my_json_dumps)
#     seasonsInfo = JSONField(null=True, json_dumps=my_json_dumps)
#     persons = JSONField(null=True, json_dumps=my_json_dumps)
#     lists = JSONField(null=True, json_dumps=my_json_dumps)
#     typeNumber = peewee.IntegerField(null=True)
#     alternativeName = peewee.TextField(null=True)
#     enName = peewee.TextField(null=True)
#     names = JSONField(null=True, json_dumps=my_json_dumps)
#     budget = JSONField(null=True, json_dumps=my_json_dumps)
#     color = peewee.TextField(null=True)
#     movieLength = peewee.TextField(null=True)
#     networks = peewee.TextField(null=True)
#     shortDescription = peewee.TextField(null=True)
#     subType = peewee.TextField(null=True)
#     fees = JSONField(null=True, json_dumps=my_json_dumps)
#     updatedAt = peewee.TextField(null=True)
#     ratingMpaa = peewee.TextField(null=True)
#     technology = JSONField(null=True, json_dumps=my_json_dumps)
#     ticketsOnSale = peewee.IntegerField(null=True)
#     similarMovies = JSONField(null=True, json_dumps=my_json_dumps)
#     sequelsAndPrequels = JSONField(null=True, json_dumps=my_json_dumps)
#     ageRating = peewee.IntegerField(null=True)
#     logo = JSONField(null=True, json_dumps=my_json_dumps)
#     imagesInfo = JSONField(null=True, json_dumps=my_json_dumps)
#     watchability = JSONField(null=True, json_dumps=my_json_dumps)
#     releaseYears = JSONField(null=True, json_dumps=my_json_dumps)
#     top10 = peewee.TextField(null=True)
#     top250 = peewee.IntegerField(null=True)
#     deletedAt = peewee.TextField(null=True)
#     isSeries = peewee.IntegerField(null=True)
#     seriesLength = peewee.IntegerField(null=True)
#     totalSeriesLength = peewee.TextField(null=True)
#     videos = JSONField(null=True, json_dumps=my_json_dumps)
#     audience = JSONField(null=True, json_dumps=my_json_dumps)
#     collections = JSONField(null=True, json_dumps=my_json_dumps)
#     createdAt = JSONField(null=True, json_dumps=my_json_dumps)
#
#
# db.connect()

Base.metadata.create_all(engine)
logger.debug('БД была создана')
if __name__ == '__main__':
    print('asd')
    s = User(name='asd', user_id=123453)
    print(s)
    session.add(s)
    session.commit()
    # user = session.query(User).first()
    # print(user.name)
    # session.rollback()
    # session.commit()
    # user = session.query(User).one_or_none()
    # print(user)

    # d = User()
    # print(d)
    # session.add(d)
    # session.commit()
    # print(d)
    # print(default_path)
    # print(db_path)
