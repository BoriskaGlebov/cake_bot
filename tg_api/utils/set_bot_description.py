from aiogram import Bot


async def set_description(bot: Bot):
    """Устанавливаю описание бота"""
    inf = await bot.get_me()
    await bot.set_my_description(f'{inf.first_name} приветствует тебя!\n'
                                 f'Этот 🤖 БОТ поможет вам выбрать десерт вашей мечты\n'
                                 f'🧁👉 бенто торт\n'
                                 f'🧁👉 кейк попс\n'
                                 f'описание приблизительное можно написать все что угодно️')
