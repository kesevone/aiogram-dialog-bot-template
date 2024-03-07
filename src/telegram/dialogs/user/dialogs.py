from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Jinja

from . import states, getters
from .. import texts

start_dialog = Dialog(
    Window(
        Jinja(texts.START_TEXT),
        getter=getters.get_user_data,
        state=states.StartDialog.MAIN
    )
)