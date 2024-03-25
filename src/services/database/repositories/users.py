from typing import List, Optional, Union

from sqlalchemy import select

from src.services.database.models import DBUser
from .base import BaseRepository


class UsersRepository(BaseRepository):
    async def get(
            self,
            user_id: int = None,
            telegram_id: int = None
    ) -> Union[Optional[DBUser], Optional[List[DBUser]]]:
        statement = (
            select(DBUser)
            .where(
                (DBUser.id == user_id) | (not user_id),
                (DBUser.telegram_id == telegram_id) | (not telegram_id)
            )
        )

        if not user_id and telegram_id:
            results = await self._session.scalars(statement)
            return results.unique().all()

        result = await self._session.scalar(statement)
        return result