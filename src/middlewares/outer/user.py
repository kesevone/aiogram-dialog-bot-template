from __future__ import annotations

from typing import Any, Awaitable, Callable, Optional

from aiogram import BaseMiddleware
from aiogram.types import Chat, TelegramObject, User

from src.services.database import DBUser
from src.utils.logger import database as logger
from ...services.database import Repository, UoW


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Optional[Any]:
        aiogram_user: Optional[User] = data.get('event_from_user')
        chat: Optional[Chat] = data.get('event_chat')
        if aiogram_user is None or chat is None or aiogram_user.is_bot:
            return await handler(event, data)

        repository: Repository = data['repo']
        user: Optional[DBUser] = await repository.user.get(telegram_id=aiogram_user.id)
        if not user:
            uow: UoW = data['uow']
            user = DBUser.create(user=aiogram_user)
            uow.add(user)
            await uow.commit()
            logger.info('New user in database: %s (%d)', aiogram_user.full_name, aiogram_user.id)

        data['user'] = user
        return await handler(event, data)