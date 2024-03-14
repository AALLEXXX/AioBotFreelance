from aiogram.filters import Filter
from aiogram.types import Message

from core.database.requests import UserDAO


class IsFirstStart(Filter):
    async def __call__(self, msg: Message) -> bool:
        chat_id = msg.from_user.id
        username = msg.from_user.username
        if await UserDAO.find_by_id(chat_id):
            return False
        await UserDAO.add(chat_id=chat_id, tg_username=username, role="user")
        return True
