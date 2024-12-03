import asyncio

import aiogram

from aiogram import Bot, Dispatcher

from Settings import bot_TOKEN

bot = Bot(token=bot_TOKEN)
dp = Dispatcher()


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
