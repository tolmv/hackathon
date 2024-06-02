from config import TOKEN
from app.handlers import router
from database.models import create_pool, init_db
import logging
import asyncio
from aiogram import Bot, Dispatcher


API_TOKEN = TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()



async def main():

    global session_factory, engine
    session_factory, engine = await create_pool()
    await init_db(engine)
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":

    #logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
