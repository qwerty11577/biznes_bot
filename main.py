import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.session.aiohttp import AiohttpSession
from aiohttp_socks import ProxyConnector
import aiohttp
from config import BOT_TOKEN
import database as db
from handlers import start, daromad, nasiya, tovar, hisobot

async def main():
    logging.basicConfig(level=logging.INFO)

    connector = ProxyConnector.from_url("socks5://103.231.12.249:1080")
    session = AiohttpSession()
    session._connector = connector

    bot = Bot(token=BOT_TOKEN, session=session)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start.router)
    dp.include_router(daromad.router)
    dp.include_router(nasiya.router)
    dp.include_router(tovar.router)
    dp.include_router(hisobot.router)

    await db.init_db()
    print("✅ Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())