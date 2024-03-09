from typing import Optional
from aiogram.types import CallbackQuery, Message
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from core.utils.delayed_course_messages import schedule_course_messages
from core.keyboards.inline import get_return_builder
from core.utils.statesPromo import StepsPromo
from core.database.requests import PromocodeDAO, PurchaseDAO, CourseDAO, UserDAO
from core.database.models import Course, Promocode
from datetime import datetime
from core.keyboards.inline import get_return_builder
from apscheduler.schedulers.asyncio import AsyncIOScheduler


#call.data - activate_promo
async def promo_handler(call: CallbackQuery, bot: Bot, state: FSMContext):
    msg_id = call.message.message_id
    chat_id = call.message.chat.id
    await bot.delete_message(chat_id, msg_id)
    await state.set_state(StepsPromo.WAITING_PROMO_FROM_USER)

    await call.message.answer(text='Отправьте промокод, который хотите активировать\nДля отмены вернитесь в меню ', reply_markup=get_return_builder().as_markup())



async def check_promo_code(promo: str) -> Optional[Promocode]:
    promo_model_list: list = await PromocodeDAO.get_all_by_params(promo=promo)
    if len(promo_model_list) == 0:
        return None
    return promo_model_list[0]

async def activate_promo_code(promo_model: Promocode, user_id: int) -> None:
    promo_id = promo_model.id
    course_id = promo_model.course_id

    await PurchaseDAO.add(user_chat_id=user_id, 
                            purchase_date=datetime.now(),
                            course_id=course_id,
                            status='promo',
                            promo_id=promo_id
                            )
    
    await PromocodeDAO.update_by_id(model_id=promo_id, is_active=True)

async def catch_users_promo(msg: Message, bot: Bot, state: FSMContext , apscheduler: AsyncIOScheduler):
    if msg.content_type != 'text': 
        return await msg.answer(f'Промокод нужно отправлять в формате текста. Попробуйте снова')

    promo = msg.text
    promo_model = await check_promo_code(promo)
    if promo_model is None:
        return await msg.answer(text='Промокод не найден. Попробуйте снова')
    
    promo_is_active = promo_model.is_active
    if not promo_is_active:
        course_model: Course = (await CourseDAO.get_all_by_params(id=promo_model.course_id))[0]
        course_name = course_model.name
        unpurchased_courses: list = await UserDAO.get_names_unpurchased_courses(user_id=msg.from_user.id)
        if course_name in unpurchased_courses:
            course_id  = course_model.id
            await activate_promo_code(promo_model, msg.from_user.id)
            await schedule_course_messages(chat_id=msg.from_user.id,
                                        course_id=course_id,
                                        apscheduler=apscheduler
                                        )
            await msg.answer(text=f'Успешно\nВы получили доступ к курсу {course_name}')
            return await state.clear()
        return await msg.answer(text=f'У вас уже есть доступ к курсу {course_name}')
    await msg.answer(text=f'Промокод уже активирован')
    await state.clear()


    



