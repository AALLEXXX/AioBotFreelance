from aiogram.filters import Filter
from aiogram.types import Message

from core.database.requests import UserDAO


class IsAuth(Filter):
    async def __call__(self, msg: Message) -> bool:
        chat_id = msg.from_user.id
        if await UserDAO.find_reg_user_by_id(chat_id) is None:
            return True
        return False
