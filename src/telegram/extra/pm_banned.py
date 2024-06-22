from __future__ import annotations

from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import ChatMemberUpdatedFilter, JOIN_TRANSITION, LEAVE_TRANSITION
from aiogram.types import ChatMemberUpdated

from src.services.database import DBUser, Gateway

router = Router(name=__name__)
router.my_chat_member.filter(F.chat.type == ChatType.PRIVATE)


@router.my_chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION))
async def set_user_active(_: ChatMemberUpdated, user: DBUser, gateway: Gateway):
    user.is_active = True
    return await gateway.commit(user)


@router.my_chat_member(ChatMemberUpdatedFilter(LEAVE_TRANSITION))
async def set_user_inactive(_: ChatMemberUpdated, user: DBUser, gateway: Gateway):
    user.is_active = False
    return await gateway.commit(user)
