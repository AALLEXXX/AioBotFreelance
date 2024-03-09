from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
import random
from aiogram import Bot
import string
from typing import List, Tuple
from aiogram.types import Message, CallbackQuery
from core.database.models import Course
from core.database.requests import CourseDAO, PromocodeDAO

def get_promo(quantity: int) -> list[str]:
    promo_list = []
    for i in range(quantity):
        letters_and_digits = string.ascii_lowercase + string.digits
        rand_string = ''.join(random.sample(letters_and_digits, 10))
        promo_list.append(rand_string)
    return promo_list


# /promo
async def get_promo_command(msg: Message, state: FSMContext):
    course_models: List[Course] = await CourseDAO.get_all_by_params()
    courses_names: List[Tuple[str]] = [(i.name) for i in course_models]
    builder = InlineKeyboardBuilder()
    for i in courses_names:
        builder.button(text=f'{i}', callback_data=f'promo_{i}')    
    await msg.answer(text='Выберите на какой курс хотите получить промокод', reply_markup=builder.as_markup())


#call.data = promo_ + course name
async def choice_number_promocodes(call : CallbackQuery, bot: Bot): 
    
    await bot.delete_message(call.from_user.id, call.message.message_id)


    course = call.data.split('_')[-1]

    builder = InlineKeyboardBuilder()
    builder.button(text=f'1 промокод', callback_data=f'getpromo_{course}_1')    
    builder.button(text=f'5 промокодов ', callback_data=f'getpromo_{course}_5')    
    builder.button(text=f'10 промокодов', callback_data=f'getpromo_{course}_10')    

    await call.message.answer(text='Выберите сколько промокодов хотите получить', reply_markup=builder.as_markup())
    


async def get_promocodes(call: CallbackQuery, bot: Bot):

    await bot.delete_message(call.from_user.id, call.message.message_id)

    _, course_name, quantity = call.data.split('_')
    quantity = int(quantity)
    rand_strings: list = get_promo(quantity)   
    course: list = await CourseDAO.get_all_by_params(name=course_name)
    course_id = course[0].id if course else None
    try:
        for i in rand_strings:
            await PromocodeDAO.add(promo=i, course_id=course_id) 
    finally:
        pass
    promo_text = '\n\n'.join(rand_strings)

    await call.message.answer(text=f'Промкод(ы) для {course_name}:\n\n{promo_text}')