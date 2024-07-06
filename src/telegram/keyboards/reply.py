from typing import Optional

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def build_reply_keyboard(
    *texts: str,
    resize_keyboard: Optional[bool] = True,
    one_time_keyboard: Optional[bool] = False,
    row_width: Optional[int] = 2,
) -> ReplyKeyboardMarkup:
    builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

    builder.add(*[KeyboardButton(text=text) for text in texts])
    builder.adjust(row_width)

    return builder.as_markup(
        resize_keyboard=resize_keyboard,
        one_time_keyboard=one_time_keyboard,
    )
