from aiogram.types import Message
from core.database.requests import UserDAO
import openpyxl

from datetime import datetime
from aiogram.types import FSInputFile



async def make_excel_users_file() -> str:
    """
    making excel file and return file name 
    """
    users_models: list = await UserDAO.get_all_by_params()
    users = [[i.chat_id, i.fullname, i.role, 
              i.phone_number, 
              i.date_registration.strftime('%Y-%m-%d %H:%M:%S') 
              if i.date_registration else i.date_registration, i.tg_username] 
              for i in users_models]
    
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.append(['chat id', 'ФИО', 'роль', 'Номер телефона', 'дата регистрации', 'Телеграмм юзернейм'])

    for row_data in users:
        sheet.append(row_data)

    time = datetime.now().time().strftime('%H:%M:%S')
    file_name = f'users {datetime.now().date()}_{time}.xlsx'
    wb.save(f'core/users_excel_files/{file_name}')
    return file_name


# command - /get_users_data 
async def get_excel_usersdata_file(msg: Message) -> Message:
    file_name: str = await make_excel_users_file()

    file_path: str = f'core/users_excel_files/{file_name}'

    return await msg.reply_document(document=FSInputFile(path=file_path),)

