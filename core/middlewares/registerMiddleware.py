from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware, Bot
from aiogram.types import Message
from core.database.requests import User


class RegisterMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        chat_id = event.from_user.id

        if await User.find_by_id(chat_id):
            return await handler(event, data)
        data["hello"] = "hello"
        return await handler(event, data)
