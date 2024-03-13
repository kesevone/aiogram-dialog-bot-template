from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram_dialog import DialogManager

from src.telegram.dialogs.user import states

router = Router(name=__name__)


class MainHandlers:

    @staticmethod
    @router.message(CommandStart())
    async def start_main_dialog(_: types.Message, dialog_manager: DialogManager):
        return await dialog_manager.start(states.MainDialog.START)