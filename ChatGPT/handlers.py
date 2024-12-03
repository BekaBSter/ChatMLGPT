from aiogram.filters import CommandStart
from aiogram.types import Message
from Settings import DEBUG, out
from aiogram import Router
import ChatGPT.keyboards as kb
import Database

router = Router()


# Начало работы с ботом посредством команды Start
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.delete()
    await message.answer("Привет!")
    await Database.new_user(message.from_user.id)
    if DEBUG:
        out("Бот: Успешно выполнен обработчик команды /start. "
            f"Пользователь: {message.from_user.first_name}. "
            f"User ID: {message.from_user.id}.\n", "g")
