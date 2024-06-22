from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent
from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram_dialog.api.exceptions import OutdatedIntent, UnknownIntent

from src.telegram.dialogs.user.main import states

from src.utils.logger import service

router = Router()


@router.errors(ExceptionTypeFilter(UnknownIntent, OutdatedIntent))
async def on_intent_error(event: ErrorEvent, dialog_manager: DialogManager):
    # Handling UnknownIntent and OutdatedIntent Error, starting new dialog.
    service.error("Restarting dialog: %s", event.exception)
    if event.update.callback_query:
        await event.update.callback_query.answer(
            """
Не удалось найти диалог.
Возвращаемся в главное меню.
            """,
        )
        if event.update.callback_query.message:
            try:
                await event.update.callback_query.message.delete()
            except TelegramBadRequest:
                pass
    elif event.update.message:
        await event.update.message.answer(
            """
Не удалось найти диалог.
Возвращаемся в главное меню.
            """,
        )
    await dialog_manager.start(
        states.StartDialogSG.WELCOME,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.SEND,
    )
