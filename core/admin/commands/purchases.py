from datetime import datetime
from aiogram.types import Message
from aiogram.types import FSInputFile
from core.database.requests import PurchaseDAO
from core.excel.excel_utility import make_excel_file


# command - /get_users_purchases
async def get_excel_purchases_file(msg: Message) -> Message:
    data = await PurchaseDAO.get_users_purchases()
    data = [list(row) for row in data]
    time: str = datetime.now()
    file_name: str = f"платежи {datetime.now().date()}_{time}.xlsx"
    file_path: str = "core/excel/purchases_excel_files/"

    name_colums = [
        "Дата создания счета",
        "Стоимость",
        "Статус",
        "Имя",
        "Фамилия",
        "Отчество",
        "Роль",
        "Дата регистрации",
        "Название курса",
    ]
    await make_excel_file(data, file_path, file_name, names_colums=name_colums)

    return await msg.reply_document(document=FSInputFile(path=file_path + file_name))
