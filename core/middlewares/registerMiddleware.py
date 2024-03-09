from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware, Bot
from aiogram.filters import Command
from aiogram.types import Message, TelegramObject, Update, CallbackQuery
from core.database.requests import User
from core.keyboards.inline import get_but_for_start_registration
from core.utils.statesregister import StepsRegister
from aiogram.fsm.storage.base import BaseStorage


class RegisterMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        chat_id = event.from_user.id

        if await User.find_by_id(chat_id): 
            return await handler(event, data)
        data['hello'] = 'hello'
        return await handler(event, data)
        # await self.bot.delete_message(chat_id=chat_id, message_id=event.message.message_id)
        # await event.message.answer(text='Вы не зарегистрированы. \nЧтобы пользоваться ботом, необходима регистрация.\nНажмите начать, чтобы перейти в режим регистрации', reply_markup=get_but_for_start_registration())

            
