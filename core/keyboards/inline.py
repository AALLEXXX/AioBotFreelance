from typing import List, Tuple
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_menu_keyboard_builder() -> InlineKeyboardBuilder:
    key_builder = InlineKeyboardBuilder()
    key_builder.button(text="Подробнее о курсах ℹ️", callback_data="info")
    key_builder.button(text="Выбрать обучение 📚", callback_data="payment_course")
    key_builder.button(text="Активировать промокод ✍️", callback_data="activate_promo")
    key_builder.button(text="Задать вопрос ❔", callback_data="question")
    # key_builder.button(text='test',
    #                    callback_data='test')
    key_builder.adjust(1)
    return key_builder


def get_but_for_start_registration():
    key_builder = InlineKeyboardBuilder()
    key_builder.button(text="Начать 📝", callback_data="start_registration")
    key_builder.button(text="Вернуться в главное меню ⬅️", callback_data="return")

    key_builder.adjust(1)
    return key_builder.as_markup()


def get_return_builder():
    key_builder = InlineKeyboardBuilder()
    key_builder.button(text="Вернуться в главное меню ⬅️", callback_data="return")
    return key_builder


def get_state_manager_but():
    key_builder = InlineKeyboardBuilder()
    key_builder.button(text="Все верно ✅", callback_data="next")
    key_builder.button(text="Повторить 🔃", callback_data="back")
    return key_builder.as_markup()


def get_board_for_FS_handler(courses: List[Tuple[str]]) -> InlineKeyboardBuilder:

    key_builder = InlineKeyboardBuilder()
    for course_name in courses:
        key_builder.button(text=f"{course_name}", callback_data=f"course_{course_name}")
    return key_builder


def get_return_to_start_massage_but():
    key_builder = InlineKeyboardBuilder()
    key_builder.button(text="Вернуться к информации о курсах ⬅️", callback_data="info")
    return key_builder.as_markup()
