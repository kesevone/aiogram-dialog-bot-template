from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Jinja

import src.telegram.dialogs.common.getters
from . import states, getters, texts

main_dialog = Dialog(
    Window(
        Jinja(texts.WELCOME_TEXT),
        getter=src.telegram.dialogs.common.getters.get_user_data,
        state=states.MainDialog.START
    )
)
