from aiogram.fsm.state import State, StatesGroup


class StepsSupport(StatesGroup):
    GET_USER_QUESTION_MSG = State()
    GET_ADMIN_ANSWER = State()