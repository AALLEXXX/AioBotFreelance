from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import Bot
from core.database.models import Course
from core.keyboards.inline import (
    get_but_for_start_registration,
    get_return_to_start_massage_but,
)
from core.handlers.basic import get_menu
from core.handlers.first_start_handler import first_user_start_handler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from core.database.requests import CourseDAO, PurchaseDAO
from aiogram.exceptions import TelegramBadRequest


# call.data - info
async def get_info_handler(call: CallbackQuery, bot: Bot):
    msg_id = call.message.message_id
    chat_id = call.message.chat.id
    await bot.delete_message(chat_id, msg_id)
    await first_user_start_handler(call.message)


# call.data - return
async def back_to_menu_button_handler(call: CallbackQuery, bot: Bot, state: FSMContext):
    msg_id = call.message.message_id
    chat_id = call.message.chat.id
    try:
        await bot.delete_message(chat_id, msg_id)
    except TelegramBadRequest:
        pass
    finally:
        await state.clear()
        await get_menu(call.message)


# call.data - course + course name
async def first_course_handler(call: CallbackQuery, bot: Bot):  # TODO
    msg_id = call.message.message_id
    chat_id = call.message.chat.id
    await bot.delete_message(chat_id, msg_id)

    course_name = call.data.split("_")[-1]

    course_model: Course = (await CourseDAO.get_all_by_params(name=course_name))[0]

    await call.message.answer(
        text=f"{course_model.description}",
        reply_markup=get_return_to_start_massage_but(),
    )


# call.data - any
async def check_registration_handler(call: CallbackQuery, bot: Bot):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await call.message.answer(
        "Вы не зарегистрированы ❗️", reply_markup=get_but_for_start_registration()
    )


async def test_send_mes(bot: Bot, chat_id: int, text: str):
    await bot.send_message(chat_id=chat_id, text=f"{text}")


# call.data - test
async def test_handler(call: CallbackQuery, bot: Bot, apscheduler: AsyncIOScheduler):
    a = await PurchaseDAO.get_users_purchases()
    a = [list(row) for row in a]
