from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup



def get_choice_course_to_pay_markup(courses: list) -> InlineKeyboardMarkup:
    key_builder =  InlineKeyboardBuilder()

    if len(courses) != 0: 
        for course in courses:
            key_builder.button(text=f'{course}',
                        callback_data=f'pay_course_{course}')

    key_builder.button(text='Вернуться в меню',
                        callback_data='return')
    key_builder.adjust(1)
    return key_builder.as_markup()   

def get_yes_no_payment_builder(course_name: str) -> InlineKeyboardBuilder:
    key_builder =  InlineKeyboardBuilder()
    key_builder.button(text='Подтверждаю',
                        callback_data=f'ready_to_pay_course_{course_name}')
    key_builder.button(text='Вернуться в меню',
                        callback_data='return')
    key_builder.adjust(1)
    return key_builder

def get_payment_builder(
                        course_name: str,
                        url: str = 'https://www.youtube.com/watch?v=K8x4a44rD80'
                        ) -> InlineKeyboardBuilder:
    
    key_builder =  InlineKeyboardBuilder()
    key_builder.button(text='Оплатить', url=url)
    key_builder.button(text='Я оплатил',
                        callback_data=f'paid_{course_name}')
    key_builder.adjust(1)
    return key_builder