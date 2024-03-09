import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from core.filters.isadmin import IsAdmin
from core.admin.commands.admin import admin_panel
from core.admin.commands.promocode import get_promo_command, choice_number_promocodes, get_promocodes
from core.admin.commands.user_data_to_excel import get_excel_usersdata_file

from settings import settings
from aiogram import F

from core.handlers.basic import get_menu
from core.utils.commands import set_commands
from core.handlers.payment_callback import buying_course_handler, check_payment_handler, choice_course_buts_handler, confirm_course_selection_handler
from core.handlers.promo_handlers import catch_users_promo, promo_handler
from core.handlers.first_start_handler import first_user_start_handler
from core.handlers.support import  admin_answer_to_user, waiting_message_from_user_handler, question_but_handler
from core.handlers.callback import back_to_menu_button_handler, check_registration_handler,  first_course_handler,\
                                    get_info_handler,\
                                     test_handler
from core.handlers.registrationForm import handler_accept_but, handler_back_but, handler_user_reg_data, registration_but_handler
from core.handlers.support import admin_answer_but_handler
from core.filters.isauth import IsAuth
from core.filters.isfirststart import IsFirstStart
from core.utils.statesRegister import StepsRegister
from core.utils.statesSupport import StepsSupport
from core.utils.statesPromo import StepsPromo

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from core.middlewares.apschedulerMiddleware import SchedulerMiddleware
from aiogram.fsm.storage.redis import RedisStorage
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler_di import ContextSchedulerDecorator


async def start() -> None:

    bot = Bot(token=settings.bots.bot_token)
    storage = RedisStorage.from_url(f'redis:{settings.REDIS_URL}')
    dp = Dispatcher(storage=storage)
    jobstores = {
        'default' : RedisJobStore(jobs_key='dispatcher_trips_jobs',
                                  run_times_key='dispatched_trips_running',
                                  host='localhost',
                                  db=2,
                                  port=6379
        )

    }
    await set_commands(bot)

    scheduler = ContextSchedulerDecorator(AsyncIOScheduler(timezone='Europe/Moscow', jobstores=jobstores))
    scheduler.ctx.add_instance(bot, declared_class=Bot)
    scheduler.start()

    dp.update.middleware.register(SchedulerMiddleware(scheduler))
    dp.message.register(first_user_start_handler, IsFirstStart())
    dp.callback_query.register(first_course_handler, F.data.startswith('course'))
    
 


    dp.callback_query.register(test_handler, F.data.startswith('test'))
    dp.message.register(get_menu, CommandStart())
    dp.callback_query.register(back_to_menu_button_handler, F.data.startswith('return'))
    dp.callback_query.register(get_info_handler, F.data.startswith('info'))
    dp.callback_query.register(question_but_handler, F.data.startswith('question'))
    dp.callback_query.register(admin_answer_but_handler, F.data.startswith('admin_take_question'))

    dp.message.register(admin_answer_to_user, StepsSupport.GET_ADMIN_ANSWER)
    dp.message.register(waiting_message_from_user_handler, StepsSupport.GET_USER_QUESTION_MSG)

    
    """-----------------------------------------------------------"""
    #registration
    dp.callback_query.register(registration_but_handler, F.data.startswith('start_registration'))
    dp.callback_query.register(handler_accept_but, F.data.startswith('next'))
    dp.callback_query.register(handler_back_but, F.data.startswith('back'))
    dp.message.register(handler_user_reg_data, StepsRegister.GET_FULL_NAME)
    dp.message.register(handler_user_reg_data, StepsRegister.GET_PHONE)


    """-----------------------------------------------------------"""
    dp.callback_query.register(check_registration_handler, IsAuth())
    dp.message.register(admin_panel, Command('admin'), IsAdmin())
    dp.message.register(get_promo_command, Command('promo'), IsAdmin())
    dp.message.register(get_excel_usersdata_file, Command('get_users_data'), IsAdmin())
    dp.callback_query.register(choice_number_promocodes, F.data.startswith('promo_'), IsAdmin())
    dp.callback_query.register(get_promocodes, F.data.startswith('getpromo_'), IsAdmin())

    dp.callback_query.register(promo_handler, F.data.startswith('activate_promo'))
    dp.message.register(catch_users_promo, StepsPromo.WAITING_PROMO_FROM_USER)

    dp.callback_query.register(choice_course_buts_handler, F.data.startswith('payment'))
    dp.callback_query.register(confirm_course_selection_handler, F.data.startswith('pay'))
    dp.callback_query.register(buying_course_handler, F.data.startswith('ready'))
    dp.callback_query.register(check_payment_handler, F.data.startswith('paid'))

    
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(start())
