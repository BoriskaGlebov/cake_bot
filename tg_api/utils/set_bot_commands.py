from aiogram import Bot
from aiogram.types import BotCommand

main_menu_commands = [
    BotCommand(command='/start',
               description='Запуск бота'),
    BotCommand(command='/cake_pops',
               description='Заказать кейк попс'),
    # BotCommand(command='/find_param',
    #            description='Подбор 🎥 по параметрам'),
    # BotCommand(command='/top_100',
    #            description='Топ 100 🎥 Кинопоиска'),
    # BotCommand(command='/history',
    #            description='📜История запросов'),
    BotCommand(command='/help',
               description='Справка по работе бота'),
    BotCommand(command='/db',
               description='Получить БД'),
]


async def set_main_menu(bot: Bot):
    """Создаем список с командами и их описанием для кнопки menu"""

    await bot.set_my_commands(main_menu_commands[:-1])


async def set_main_menu_admin(bot: Bot):
    """Создаем список с командами и их описанием для кнопки menu"""

    await bot.set_my_commands(main_menu_commands)


