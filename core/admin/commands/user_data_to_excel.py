from datetime import datetime
from typing import List
from aiogram.types import Message
from aiogram.types import FSInputFile
from core.database.requests import UserDAO

from core.excel.excel_utility import make_excel_file
from core.database.models import User

# command - /get_users_data 
async def get_excel_usersdata_file(msg: Message) -> Message:
    users_models: list = await UserDAO.get_all_by_params()
    
    users:list[list] = [[i.chat_id, i.fullname, i.role, 
              i.phone_number, 
              i.date_registration.strftime('%Y-%m-%d %H:%M:%S') 
              if i.date_registration else i.date_registration, i.tg_username] 
              for i in users_models]
    
    columns_names: List[str] = User().__table__.columns.keys()

    time = datetime.now().time().strftime('%H:%M:%S')
    file_name = f'users {datetime.now().date()}_{time}.xlsx'
    file_path: str = 'core/excel/users_excel_files/'


    await make_excel_file(users, columns_names, file_path, file_name)

    return await msg.reply_document(document=FSInputFile(path=file_path + file_name))

