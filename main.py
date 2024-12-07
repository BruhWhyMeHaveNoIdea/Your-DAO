import sys
import logging
import asyncio

from aiogram import Dispatcher

from bot.admin.handlers import router as admin_router
from bot.user.handlers import router as user_router
from bot.gpt.handlers import router as gpt_router
from bot.bot import bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import bot.user.utils as utils


from bot.db.db import create_tables
import bot.db.default_db as default_db




async def main():
    await create_tables()
    await default_db.create_default_table()
    dp = Dispatcher()
    dp.include_routers(gpt_router,admin_router, user_router)
    shed = AsyncIOScheduler(timezone='Europe/Moscow')
    shed.add_job(utils.delete_one_day, "cron", hour="23", minute=59, second=59)
    shed.start()
    await dp.start_polling(bot)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    logging.getLogger("sqlalchemy.engine.Engine").disabled = True
    asyncio.run(main())

