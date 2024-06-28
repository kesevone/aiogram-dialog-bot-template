from __future__ import annotations

from typing import Any, Awaitable, Callable, Optional

from aiogram import BaseMiddleware
from aiogram.types import Chat, TelegramObject, User

from src.database import DBUser, Gateway
from src.utils.logger import database as logger


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Optional[Any]:
        aiogram_user: Optional[User] = data.get("event_from_user")
        chat: Optional[Chat] = data.get("event_chat")
        if aiogram_user is None or chat is None or aiogram_user.is_bot:
            return await handler(event, data)

        gw: Gateway = data["gateway"]
        user: Optional[DBUser] = await gw.users.get_by_id(user_id=aiogram_user.id)
        if user is None:
            user: DBUser = DBUser.from_aiogram(user=aiogram_user)
            await gw.commit(user)
            logger.info(
                "New user in database: %s (%d)", aiogram_user.full_name, aiogram_user.id
            )

        if aiogram_user.username and user.username != aiogram_user.username:
            user.username = aiogram_user.username
            await gw.commit(user)

        if aiogram_user.full_name and user.full_name != aiogram_user.full_name:
            user.full_name = aiogram_user.full_name
            await gw.commit(user)

        data["user"] = user
        return await handler(event, data)
