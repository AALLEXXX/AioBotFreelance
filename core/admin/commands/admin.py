from aiogram.types import Message


# /admin
async def admin_panel(msg: Message):
    await msg.answer(
        text="Привет админ! Список командр:\n\n"
        "/promo - команда для генерации промокодов для пользователей\n\n"
        "/get_users_data - команда для получения excel файла с данными всех зарегистрированных пользователей"
    )
