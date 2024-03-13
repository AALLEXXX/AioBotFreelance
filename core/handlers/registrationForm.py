from sqlite3 import IntegrityError
from aiogram.types import CallbackQuery, Message
from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.context import FSMContext
from core.database.requests import UserDAO
from core.utils.statesRegister import StepsRegister
from core.handlers.basic import get_menu
from datetime import datetime
from core.keyboards.inline import get_state_manager_but

import re


def valid_fullname(full_name: str):
    pattern = r"^[A-Za-zА-Яа-я]+ [A-Za-zА-Яа-я]+([ -][A-Za-zА-Яа-я]+)?$"

    if re.match(pattern, full_name):
        return True
    return False


def validate_phone_number(phone_number):
    phone_number = phone_number.replace(" ", "")

    pattern = re.compile(r"^(8)\d{10}$")

    return bool(pattern.match(phone_number))


async def handler_user_reg_data(msg: Message, state: FSMContext):
    if msg.content_type != "text":
        return await msg.answer(
            f"Данные нужно отправлять в формате текста. Попробуйте снова"
        )

    data = msg.text
    bold_data = f"<b>{data}</b>"
    state_name = (await state.get_state()).split(":")[1]

    if state_name == "GET_FULL_NAME":
        if not valid_fullname(data):
            return await msg.answer(text="Некорректное фио. Попробуйте снова")
        await state.update_data(FULL_NAME=data)

    elif state_name == "GET_PHONE":
        if not validate_phone_number(data.strip()):
            return await msg.answer(
                text="Некорректный ввод номера телефона. Попробуйте снова"
            )
        await state.update_data(GET_PHONE=data)

    await msg.answer(
        f"Вы отправили {bold_data} ✉️\nЧтобы продолжить нажмите"
        ' "все верно ✅", если нужно повторить ввод, нажмите кнопку "повторить 🔃"',
        reply_markup=get_state_manager_but(),
        parse_mode=ParseMode.HTML,
    )


async def handler_back_but(call: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    state_name = (await state.get_state()).split(":")[1]
    msg = call.message
    if state_name == "GET_FULL_NAME":
        await msg.answer(f"Отправьте еще раз ваше ФИО 🔃")
    elif state_name == "GET_PHONE":
        await msg.answer(f"Отправьте еще раз ваш номер 🔃")


async def handler_accept_but(call: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    state_name = (await state.get_state()).split(":")[1]
    msg = call.message

    if state_name == "GET_FULL_NAME":
        await state.set_state(StepsRegister.GET_PHONE)
        await msg.answer(
            "ФИО принято ✅\nТеперь отправьте номер телефона 📲 для завершения регистрации 🔚\n"
            'Формат номера телефона "8 ххх ххх хх хх"'
        )

    elif state_name == "GET_PHONE":
        user_state_data = await state.get_data()
        fullname = user_state_data["FULL_NAME"]

        first_name, last_name, middle_name = fullname.split()

        number = user_state_data["GET_PHONE"]
        chat_id = call.from_user.id
        registration_date = datetime.now()
        try:
            await UserDAO.update_by_id(
                model_id=chat_id,
                first_name=first_name,
                last_name=last_name,
                middle_name=middle_name,
                phone_number=number,
                date_registration=registration_date,
            )

        except Exception:
            return await msg.answer(
                text="Такой номер уже зарегистрирован. Попробуйте снова"
            )

        await msg.answer(text="Номер принят ✅.\nРегистрация успешно завершена 🎉")
        await state.clear()


async def registration_but_handler(call: CallbackQuery, bot: Bot, state: FSMContext):
    msg_id = call.message.message_id
    chat_id = call.message.chat.id
    await bot.delete_message(chat_id, msg_id)
    await state.set_state(StepsRegister.GET_FULL_NAME)
    await call.message.answer(
        text="❗️Необходимо зарегистрироваться❗️\n✉️ Отправьте ФИО одним смс\n"
        'Формат фио - "Иванов Иван Иванович"'
    )
