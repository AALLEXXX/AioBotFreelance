from pickletools import StackObject
from re import S
from aiogram.types import FSInputFile, InputFile, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.database.models import Course
from core.keyboards.inline import get_board_for_FS_handler
from core.database.requests import CourseDAO
from typing import List, Tuple 



START_MESSAGE = """💵💵💵 КАК ЗАРАБАТЫВАТЬ с компанией FOHOW
Знакомство с системой построения бизнеса. 
Вводный курс ✅
🚀 УСПЕШНЫЙ СТАРТ И ПЕРВЫЕ ШАГИ

За символическую плату вы получаете доступ к материалам

✨ Именно сейчас я обучаю партнеров компании, как зарабатывать на рынке альтернативной медицины. 

Отныне все партнеры компании, гарантировано могут научиться зарабатывает от 200000 рублей в в месяц, это может каждый. Если вы достаточно мотивированы, я сделаю из вас успешного сетевого предпринимателя.


Стоимость доступа 👉🏻  всего 3553 рубля на три месяца и 15 встреч. оплатить можно из любой точки мира. 

👨🏼‍💻 Курс удобно проходить - все материалы находятся в канале телеграм👌🏻

Оплатить  и получить доступ  
👇👇👇"""

#/start
async def first_user_start_handler(msg: Message) -> None:

    course_models: list[Course] = await CourseDAO.get_all_by_params()
    courses_names: List[Tuple[str]] = [(i.name) for i in course_models]


    key_builder: InlineKeyboardBuilder = get_board_for_FS_handler(courses_names)
    key_builder.button(text='Вернуться в главное меню ⬅️',
                        callback_data='return')
    key_builder.adjust(1)

    photo = FSInputFile('core/content/images/start_img.jpg')

    await msg.answer_photo(photo=photo, caption=START_MESSAGE, reply_markup=key_builder.as_markup())