from telebot import types
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_helper import ApiTelegramException

bot = AsyncTeleBot('7660590004:AAGt_Pqj6GP4vYXmGZd-H6g5wPTFxBjK_Tc')


# Первый запуск бота
@bot.message_handler(commands=["start"])
async def start(message):
    chat_id = message.chat.id
    message_id = message.message_id
    await bot.delete_message(chat_id, message_id)
    await bot.send_message(chat_id, "Hello")
