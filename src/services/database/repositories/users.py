from typing import Optional, cast

from sqlalchemy import select

from src.services.database.models import DBUser
from .base import BaseRepository


class UserRepository(BaseRepository):
    async def get(self, user_id: int) -> Optional[DBUser]:
        return cast(
            Optional[DBUser],
            await self._session.scalar(select(DBUser).where(DBUser.id == user_id)),
        )