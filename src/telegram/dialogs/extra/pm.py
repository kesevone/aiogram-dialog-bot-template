from typing import Final

from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import ChatMemberUpdatedFilter, JOIN_TRANSITION, LEAVE_TRANSITION
from aiogram.types import ChatMemberUpdated

from src.services.database import DBUser, UoW

router = Router(name=__name__)
router.my_chat_member.filter(F.chat.type == ChatType.PRIVATE)


@router.my_chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION))
async def enable_notifications(_: ChatMemberUpdated, user: DBUser, uow: UoW) -> None:
    user.enable_notifications()
    await uow.commit(user)


@router.my_chat_member(ChatMemberUpdatedFilter(LEAVE_TRANSITION))
async def disable_notifications(_: ChatMemberUpdated, user: DBUser, uow: UoW) -> None:
    user.disable_notifications()
    await uow.commit(user)