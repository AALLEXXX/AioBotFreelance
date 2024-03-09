from aiogram import Bot
from aiogram.types import Message
from core.keyboards.inline import get_return_builder
from core.utils.statesSupport import StepsSupport
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from core.database.requests import UserDAO, UserSupportRequestDAO
from core.keyboards.support_keyboards import get_support_keyboard
from datetime import datetime


#call.data - question
async def question_but_handler(call: CallbackQuery, bot: Bot, state: FSMContext):
    msg_id = call.message.message_id
    chat_id = call.message.chat.id
    await bot.delete_message(chat_id, msg_id)
    await state.set_state(StepsSupport.GET_USER_QUESTION_MSG)
    await call.message.answer(text='Напишите свой вопрос в чат и вам скоро ответят!', reply_markup=get_return_builder().as_markup())




async def waiting_message_from_user_handler(msg: Message, bot: Bot, state: FSMContext):

    await state.clear()
    if msg.content_type != 'text': 
        return await msg.answer(f'Вопрос нужно отправлять в формате текста. Попробуйте снова')
    username = msg.from_user.username
    user_msg = msg.text 
    user_chat_id = msg.from_user.id
    msg_id = msg.message_id
    admins = await UserDAO.get_chat_id_all_admin()
    print(admins)
    await UserSupportRequestDAO.add(user_id=user_chat_id, question=user_msg, date=datetime.now())
    if len(admins) > 0: 
        for chat_id in admins:
            await bot.send_message(chat_id=chat_id[0], text=f'Вопрос от пользователя @{username}\n-----------------\n'
                                                        f'{user_msg}\n-----------------', reply_markup=get_support_keyboard(user_chat_id, msg_id).as_markup())
        await msg.answer(text='Сообщение получено и доставленно менеджерам, ожидайте ответа')
    else: 
        await msg.answer(text='Админов не найдено. Сообщение не доставленно. Возможно произошел сбой')


#call.data - admin_take_question 
async def admin_answer_but_handler(call: CallbackQuery, state: FSMContext):
    data = call.data 
    user_id = data.split('_')[-2]
    user_msg_id = data.split('_')[-1]
    await state.update_data(USER_ID = user_id)
    await state.update_data(USER_MSG_ID = user_msg_id)
    await call.message.answer(text='Отправьте ответ и он будет доставлен пользователю')
    await state.set_state(StepsSupport.GET_ADMIN_ANSWER)



async def admin_answer_to_user(msg: Message, bot: Bot, state: FSMContext):
    state_data = await state.get_data()
    user_id = state_data['USER_ID']
    user_msg_id = state_data['USER_MSG_ID']
    admin_answer = msg.text
    await bot.send_message(chat_id=user_id, reply_to_message_id=user_msg_id,text=f'Ответ от менеджера\n{admin_answer}')
    await state.clear()
    await msg.answer(text='Ваш ответ отправлен пользователю')