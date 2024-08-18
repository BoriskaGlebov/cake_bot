from aiogram import Bot
from aiogram.types import BotCommand

main_menu_commands = [
    BotCommand(command='/start',
               description='Запуск бота'),
    BotCommand(command='/find_film',
               description='Поиск 🎥 по названию'),
    BotCommand(command='/find_param',
               description='Подбор 🎥 по параметрам'),
    BotCommand(command='/top_100',
               description='Топ 100 🎥 Кинопоиска'),
    BotCommand(command='/history',
               description='📜История запросов'),
    BotCommand(command='/help',
               description='Справка по работе бота'),
    BotCommand(command='/db',
               description='Получить БД'),
]


async def set_main_menu(bot: Bot):
    """Создаем список с командами и их описанием для кнопки menu"""

    await bot.set_my_commands(main_menu_commands[:-1])


async def set_main_menu_admdin(bot: Bot):
    """Создаем список с командами и их описанием для кнопки menu"""

    await bot.set_my_commands(main_menu_commands)


async def set_discription(bot: Bot):
    """Устанавливаю описание бота"""
    inf = await bot.get_me()
    await bot.set_my_description(f'{inf.first_name} приветствует тебя!\n'
                                 f'Этот 🤖БОТ занимается поиском\n'
                                 f'🍿👉 фильмов\n'
                                 f'🍫👉 сериалов\n'
                                 f'Сервиса Кинопоиск⭐️')
