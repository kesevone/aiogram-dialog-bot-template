from aiogram_dialog import ShowMode
from aiogram_dialog.widgets.kbd import (
    Back,
    Button,
    Cancel,
    FirstPage,
    Group,
    Next,
    NextPage,
    PrevPage,
)
from aiogram_dialog.widgets.text import Const, Format
from magic_filter import F

from . import texts

# Custom scroll buttons for pager, only visible when there are more than one page.
# PrevPage is shown when the current page is greater than 1.
# NextPage is shown when the current page is less than the total number of pages.
ID_SCROLL_NO_PAGER = "ID_SCROLL_NO_PAGER"
CUSTOM_SCROLL_BTNS = Group(
    PrevPage(
        scroll=ID_SCROLL_NO_PAGER,
        text=Const(texts.ARROW_LEFT_BUTTON_TEXT),
        when=F["current_page1"] > 1,
    ),
    FirstPage(ID_SCROLL_NO_PAGER, text=Format("{current_page1}/{pages} стр.")),
    NextPage(
        scroll=ID_SCROLL_NO_PAGER,
        text=Const(texts.ARROW_RIGHT_BUTTON_TEXT),
        when=F["current_page1"] != F["pages"],
    ),
    when=F["pages"] > 1,
    width=3,
)

# A button to cancel any action; when clicked, the dialog closes.
CANCEL_DIALOG_BUTTON = Button(
    Const(texts.CANCEL_BUTTON_TEXT),
    id="CLOSE_DIALOG",
    on_click=lambda e, w, m: m.done(show_mode=ShowMode.DELETE_AND_SEND),
)
BACK_DIALOG_BUTTON = Cancel(Const(texts.BACK_BUTTON_TEXT))
BACK_WINDOW_BUTTON = Back(Const(texts.BACK_BUTTON_TEXT))
NEXT_WINDOW_BUTTON = Next(Const(texts.NEXT_BUTTON_TEXT))
