from aiogram import Router, F
from aiogram.filters import Command

from tg_api.keyboards.reply.keybord_find_film import get_bot_function_find_film
from tg_api.handlers.custom_handlers.common_func import *
from tg_api.states.user_state import MovieSearch

logger = logging.getLogger(f'main.tg_api.handlers.custom_handlers.{os.path.basename(__file__)}')
sys.excepthook = any_exception
router = Router()


@router.message(F.text == 'Поиск 🎥 по названию')
@router.message(Command('find_film'))
async def finder_film(message: Message, state: FSMContext):
    """Действие по нажатии кнопки поиск фильмов, отображение новых кнопок"""
    logger.debug(f'{finder_film} - начало работы')
    await message.answer('🏆Введите название фильма?', reply_markup=get_bot_function_find_film())
    await state.set_state(MovieSearch.choosing_film_name)
    logger.info(f'{finder_film} - отработало хорошо')


@router.message(MovieSearch.choosing_film_name, F.text)
async def finder(message: Message, state: FSMContext):
    """вызов функции поиска фильмов"""
    r = await state.get_state()
    await rez_finder(message, state, MovieSearch.changing_films, FilmsBase)


@router.callback_query(MovieSearch.changing_films, F.data.startswith("num_"))
async def callbacks_films(callback: CallbackQuery, state: FSMContext):
    """Работа кнопок"""
    await callbacks_num(callback, state, MovieSearch.changing_films)


@router.message(MovieSearch.changing_films, F.text)
async def change_state(message: Message, state: FSMContext):
    """Поиск фильма без команды поиска"""
    await state.set_state(MovieSearch.choosing_film_name)
    r = await state.get_state()
    await rez_finder(message, state, MovieSearch.changing_films, FilmsBase)
