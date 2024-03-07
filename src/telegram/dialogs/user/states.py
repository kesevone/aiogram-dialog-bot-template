from aiogram.fsm.state import StatesGroup, State


class StartDialog(StatesGroup):
    MAIN = State()