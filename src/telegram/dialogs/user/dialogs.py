from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Jinja

from . import states, texts
from ..common import getters as common_getters

main_dialog = Dialog(
    Window(
        Jinja(texts.WELCOME_TEXT),
        getter=common_getters.get_user_data,
        state=states.MainDialog.START
    )
)
