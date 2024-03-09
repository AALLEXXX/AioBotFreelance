from aiogram.fsm.state import State, StatesGroup

class StepsRegister(StatesGroup):
    GET_FULL_NAME = State()
    GET_PHONE = State()

