from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager

from . import states

router = Router(name=__name__)


@router.message(CommandStart())
async def start_main_dialog(_: Message, dialog_manager: DialogManager):
    return await dialog_manager.start(states.StartDialogSG.WELCOME)
