from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text)
async def echo(message: Message):
    """"ЭХО бот"""
    await message.answer('Когда я что-то не знаю, то отвечаю повторением вашей фразы')
    await message.reply(message.text)
