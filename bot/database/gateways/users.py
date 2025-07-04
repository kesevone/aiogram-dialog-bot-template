from typing import Optional, Sequence

from sqlalchemy import func, or_, ScalarResult, select

from bot.database.models import DBUser
from .base import BaseGateway
from ..types import LoadOption, OrderByOption


class UsersGateway(BaseGateway):
    async def get_by_id(
        self,
        user_id: int,
        load: Optional[LoadOption] = None,
    ) -> Optional[DBUser]:
        self._stmt = select(DBUser).where(DBUser.id == user_id)

        self._load(load)

        return await self._session.scalar(self._stmt)

    async def get_by_username(
        self,
        username: str,
        load: Optional[LoadOption] = None,
        order_by: Optional[OrderByOption] = None,
        limit: Optional[int] = None,
    ) -> Optional[DBUser]:
        self._stmt = select(DBUser).where(
            func.lower(DBUser.username) == username.lower()
        )

        self._load(load)
        self._order_by(order_by)
        self._limit(limit)

        return await self._session.scalar(self._stmt)

    async def get_all(
        self,
        is_active: Optional[bool] = None,
        load: Optional[LoadOption] = None,
        order_by: Optional[OrderByOption] = None,
        limit: Optional[int] = None,
    ) -> Sequence[Optional[DBUser]]:
        self._stmt = select(DBUser).where(
            or_(DBUser.is_active == is_active, is_active is None)
        )

        self._load(load)
        self._order_by(order_by)
        self._limit(limit)

        results: ScalarResult = await self._session.scalars(self._stmt)
        return results.unique().all()
