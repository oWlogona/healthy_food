from aiogram import executor

from database.database import create_db
from loader import bot


async def on_startup(dp):
    await create_db()


async def on_shutdown(dp):
    await bot.close()


if __name__ == '__main__':
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)
