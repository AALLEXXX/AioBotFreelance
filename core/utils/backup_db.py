from aiogram import Bot
from aiogram.types import FSInputFile
from config import settings
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from datetime import datetime, date, time, timezone

async def send_mes(bot: Bot, chat_id : int, path: str):
    doc = FSInputFile(path)
    await bot.send_document(chat_id=chat_id, document=doc, caption="База данных")


async def schedule_backup_db_file(apscheduler: AsyncIOScheduler):
    apscheduler.add_job(send_mes, trigger='cron', 
                        hour='23', minute='59', second='0',
                        kwargs={'chat_id': settings.ADMIN_ID, 'path': r"core/database/TgBotDb.sqlite3"})