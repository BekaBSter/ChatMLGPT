import asyncio
import logging

from aiogram import Bot, Dispatcher

from Settings import BOT_TOKEN, DEBUG, out

from main_handlers import router

from Database import init_tables

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Главная функция запуска бота
async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


# Точка входа в скрипт
if __name__ == '__main__':
    # Инициализация таблиц
    init_tables()
    # Включение дополнительного логирования
    if DEBUG:
        logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt as e:
        out("Остановка бота!", "r")
