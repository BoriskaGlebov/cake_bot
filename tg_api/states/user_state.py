from aiogram.fsm.state import StatesGroup, State


class MovieSearch(StatesGroup):
    choosing_film_name = State()
    changing_films = State()
    choosing_top_100 = State()
    changing_films_top_100 = State()
    choosing_find_film_param = State()
    changing_films_find_film_param = State()
    find_film_param = State()
    choosing_year = State()
    choosing_rating = State()
    choosing_genres = State()
    choosing_country = State()
    choosing_db = State()


