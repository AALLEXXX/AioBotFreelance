from typing import List, Tuple
from aiogram.filters import Filter
from aiogram.types import Message

from core.database.requests import UserDAO

class IsAdmin(Filter):
    async def __call__(self, msg: Message) -> bool:
        chat_id = msg.from_user.id
        admins: List[Tuple[str,]] = await UserDAO.get_chat_id_all_admin()
        if any(chat_id_tuple[0] == chat_id for chat_id_tuple in admins):
            return True
        return False