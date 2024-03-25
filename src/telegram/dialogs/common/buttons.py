from aiogram_dialog.widgets.kbd import Back, Cancel, Next, Group, PrevPage, NextPage
from aiogram_dialog.widgets.text import Const, Format
from magic_filter import F

from . import texts

ID_SCROLL_NO_PAGER = 'ID_SCROLL_NO_PAGER'

CUSTOM_SCROLL_BTNS = Group(
    PrevPage(
        scroll=ID_SCROLL_NO_PAGER,
        text=Format(texts.ARROW_LEFT_BUTTON_TEXT),
        when=F['current_page1'] != F['target_page1'] & F["pages"] > 1,
    ),
    NextPage(
        scroll=ID_SCROLL_NO_PAGER,
        text=Format(texts.ARROW_RIGHT_BUTTON_TEXT),
        when=F['current_page1'] != F['target_page1'] & F["pages"] > 1
    ),
    width=2
)

BACK_DIALOG_BUTTON = Cancel(Const(texts.BACK_BUTTON_TEXT))

BACK_WINDOW_BUTTON = Back(Const(texts.BACK_BUTTON_TEXT))
NEXT_WINDOW_BUTTON = Next(Const(texts.NEXT_BUTTON_TEXT))