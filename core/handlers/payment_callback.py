import random
import string
from typing import Any, Tuple
from aiogram import Bot
from aiogram.types import CallbackQuery, Message
from yoomoney import Client, History, Quickpay
from core.keyboards.payment_inline import (
    get_choice_course_to_pay_markup,
    get_payment_builder,
    get_yes_no_payment_builder,
)
from core.database.requests import PurchaseDAO, UserDAO, CourseDAO
from core.database.models import Course
import datetime as dt
from settings import settings
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from core.utils.delayed_course_messages import schedule_course_messages
from aiogram.fsm.context import FSMContext


# call.data - payment
async def choice_course_buts_handler(call: CallbackQuery, bot: Bot) -> None:
    msg_id: int = call.message.message_id
    chat_id: int = call.message.chat.id
    await bot.delete_message(chat_id, msg_id)
    courses: list = await UserDAO.get_names_unpurchased_courses(chat_id)
    if len(courses) > 0:
        await call.message.answer(
            text="Выберите курс, который хотите преобрести",
            reply_markup=get_choice_course_to_pay_markup(courses),
        )
    else:
        await call.message.answer(
            text="Вы уже приобрели все курсы или находитель в процессе оплаты"
        )


# call.data - pay_course_ + course name
async def confirm_course_selection_handler(call: CallbackQuery, bot: Bot) -> None:
    msg_id: int = call.message.message_id
    chat_id: int = call.message.chat.id
    await bot.delete_message(chat_id, msg_id)

    course_name: str = call.data.split("_")[2]
    course = await CourseDAO.find_by_course_name(course_name=course_name)
    course_cost = course[-1]

    await call.message.answer(
        text=f"Вы выбрали курс {course_name}\n"
        f"Стоимость {course_cost} рублей\n"
        f"Подтвердите свой выбор",
        reply_markup=get_yes_no_payment_builder(course_name).as_markup(),
    )


def get_rand_string() -> str:
    letters_and_digits = string.ascii_lowercase + string.digits
    pay_token = "".join(random.sample(letters_and_digits, 10))
    return pay_token


# call.data - ready_to_pay_course_ + course name
async def buying_course_handler(
    call: CallbackQuery, bot: Bot, state: FSMContext, apscheduler: AsyncIOScheduler
) -> None:

    await bot.delete_message(call.message.chat.id, call.message.message_id)

    pay_token = get_rand_string()

    course_name = call.data.split("_")[-1]
    course = await CourseDAO.find_by_course_name(course_name=course_name)
    course_id = course[0]
    chat_id = call.from_user.id
    cost = course[-1]

    await state.update_data(COURSE=list(course))
    await state.update_data(PAY_TOKEN=pay_token)

    quickpay = Quickpay(
        receiver="4100118569930720",
        quickpay_form="shop",
        targets="Бизнес с Fohow",
        paymentType="SB",
        sum=2,
        label=pay_token,
    )

    await PurchaseDAO.add(
        user_chat_id=chat_id,
        purchase_date=dt.datetime.now(),
        course_id=course_id,
        cost=cost,
        status="не оплачен",
        pay_token=pay_token,
    )

    url = quickpay.redirected_url

    await call.message.answer(
        text='Оплатите курс. У вас есть 15 минут, после чего тикет закроется\nПосле оплаты обязательно нажмите кнопку "Я оплатил" чтобы получить доступ к курсу',
        reply_markup=get_payment_builder(url=url, course_name=course_name).as_markup(),
    )

    client = Client(settings.P2P_TOKEN)

    apscheduler.add_job(
        schedule_check_payment,
        trigger="date",
        next_run_time=dt.datetime.now() + dt.timedelta(minutes=15),  # TODO
        kwargs={"chat_id": chat_id, "pay_token": pay_token, "client": client},
    )


async def schedule_check_payment(
    bot: Bot, chat_id: int, client: Client, pay_token: str
) -> Message | None:
    history: History = client.operation_history(label=pay_token)
    if not await check_payment(history=history):
        await PurchaseDAO.delete_by_pay_token(pay_token=pay_token)
        return await bot.send_message(
            chat_id=chat_id,
            text="Вы не успели оплатить счет. Тикет закрыт.\nВы всегда можете попробовать снова",
        )


async def check_payment(history) -> bool | None:
    try:
        operation = history.operations[-1]
        if operation.status == "success":
            return True
    except Exception as e:
        return False


# call.data - paid_ + course_name
async def check_payment_handler(
    call: CallbackQuery, bot: Bot, apscheduler: AsyncIOScheduler, state: FSMContext
) -> Message | Any:
    chat_id: int = call.from_user.id
    state_data: dict = await state.get_data()
    pay_token: Any = state_data["PAY_TOKEN"]
    course: Tuple[Course.id, Course.name, Course.description, Course.cost] = state_data[
        "COURSE"
    ]
    course_id = course[0]

    client = Client(settings.P2P_TOKEN)
    history: History = client.operation_history(label=pay_token)

    if await check_payment(history=history):
        await bot.delete_message(chat_id, call.message.message_id)
        await schedule_course_messages(
            chat_id=chat_id, course_id=course_id, apscheduler=apscheduler
        )
        await PurchaseDAO.update_by_pay_token(pay_token=pay_token, status="оплачено")
        await call.message.answer(text="Оплата прошла успешно")
        return await call.message.answer(text="Вы получили доступ к курсу")  # TODO

    return await call.message.answer(text="Оплата еще идет или вы не оплатили")
