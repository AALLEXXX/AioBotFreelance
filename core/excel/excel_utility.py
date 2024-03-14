from typing import List
import openpyxl
import os


async def make_excel_file(
    data_list: list[list],
    newfile_path: str,
    newfile_name: str,
    names_colums: List[str] = None,
) -> str:
    """
    making new excel file and delete old file
    """

    files_in_directory = os.listdir(newfile_path)

    for filename in files_in_directory:
        filepath = os.path.join(newfile_path, filename)
        os.remove(filepath)

    wb = openpyxl.Workbook()
    sheet = wb.active
    if names_colums:
        sheet.append(names_colums)
    for row_data in data_list:
        sheet.append(row_data)
    wb.save(newfile_path + newfile_name)
