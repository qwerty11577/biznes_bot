import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
import database as db
from handlers import start, daromad, nasiya, tovar, hisobot, admin, excel

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start.router)
    dp.include_router(daromad.router)
    dp.include_router(nasiya.router)
    dp.include_router(tovar.router)
    dp.include_router(hisobot.router)
    dp.include_router(admin.router)
    dp.include_router(excel.router)

    await db.init_db()
    print("✅ Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())