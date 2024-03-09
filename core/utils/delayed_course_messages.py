from aiogram import Bot

from core.database.requests import Course_modulesDAO
import datetime as dt
from apscheduler.schedulers.asyncio import AsyncIOScheduler



async def send_mes(bot: Bot, chat_id : int, text: str):
    await bot.send_message(chat_id=chat_id, text=f'{text}')

async def schedule_course_messages(chat_id: int, course_id: int, apscheduler: AsyncIOScheduler):
    modules = await Course_modulesDAO.get_all_modules(course_id)
    for module in modules:
        description = module[0]
        time = module[1]
        # module_order = module[2]
        apscheduler.add_job(send_mes, trigger='date', 
                            next_run_time= dt.datetime.now() +  dt.timedelta(minutes=time), 
                            kwargs={'chat_id': chat_id,'text': description})