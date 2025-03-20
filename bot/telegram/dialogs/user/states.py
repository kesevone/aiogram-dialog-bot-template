from aiogram.fsm.state import StatesGroup, State


class StartDialogSG(StatesGroup):
    WELCOME = State()
