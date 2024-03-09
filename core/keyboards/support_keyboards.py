from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_support_keyboard(chat_id: int, user_msg_id) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text='Ответить пользователю', callback_data=f'admin_take_question_from_{chat_id}_{user_msg_id}')
    return builder
    
