from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Jinja

from .. import states
from ...common import getters as common_getters

start_dialog = Dialog(
    Window(
        Jinja(
            """
<b>Добро пожаловать</b>, {{ full_name }}!
            """
        ),
        getter=common_getters.get_db_user,
        state=states.StartDialogSG.WELCOME,
    )
)
