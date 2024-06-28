from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.database import Gateway


class DBSessionMiddleware(BaseMiddleware):
    session_pool: async_sessionmaker[AsyncSession]

    __slots__ = ("session_pool",)

    def __init__(self, session_pool: async_sessionmaker[AsyncSession]) -> None:
        self.session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            data["gateway"] = Gateway(session=session)
            return await handler(event, data)
