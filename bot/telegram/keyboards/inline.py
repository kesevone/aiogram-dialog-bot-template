from typing import Optional

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def build_inline_keyboard(
    texts: list[tuple[str, CallbackData | str]], row_width: Optional[int] = 2
) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    builder.add(
        *[InlineKeyboardButton(text=data[0], callback_data=data[1]) for data in texts]
    )
    builder.adjust(row_width)

    return builder.as_markup()
