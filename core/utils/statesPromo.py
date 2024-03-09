from aiogram.fsm.state import State, StatesGroup


class StepsPromo(StatesGroup):
    WAITING_PROMO_FROM_USER = State()


