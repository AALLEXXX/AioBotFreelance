from aiogram.types import Message, CallbackQuery
from aiogram import Bot

from core.keyboards.inline import get_menu_keyboard_builder



async def get_menu(msg : Message):
    await msg.answer('Приветствуем вас в обучающем боте 👋', reply_markup=get_menu_keyboard_builder().as_markup())





