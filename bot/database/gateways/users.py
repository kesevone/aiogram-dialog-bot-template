from typing import Any, Optional, Sequence

from sqlalchemy import ColumnElement, func, or_, ScalarResult, select
from sqlalchemy.orm import QueryableAttribute

from bot.database.models import DBUser
from .base import BaseGateway


class UsersGateway(BaseGateway):
    async def get_by_id(
        self,
        user_id: int,
        load: Optional[
            tuple[QueryableAttribute[Any]]
            | list[QueryableAttribute[Any]]
            | QueryableAttribute[Any]
        ] = None,
    ) -> Optional[DBUser]:
        self._stmt = select(DBUser).where(DBUser.id == user_id)

        self.load(load)

        return await self._session.scalar(self._stmt)

    async def get_by_username(
        self,
        username: str,
        load: Optional[
            tuple[QueryableAttribute[Any]]
            | list[QueryableAttribute[Any]]
            | QueryableAttribute[Any]
        ] = None,
        order_by: Optional[
            tuple[str | ColumnElement] | list[str | ColumnElement] | str | ColumnElement
        ] = None,
        limit: Optional[int] = None,
    ) -> Optional[DBUser]:
        self._stmt = select(DBUser).where(
            func.lower(DBUser.username) == username.lower()
        )

        self.load(load)
        self.order_by(order_by)
        self.limit(limit)

        return await self._session.scalar(self._stmt)

    async def get_all(
        self,
        is_active: Optional[bool] = None,
        load: Optional[
            tuple[QueryableAttribute[Any]]
            | list[QueryableAttribute[Any]]
            | QueryableAttribute[Any]
        ] = None,
        order_by: Optional[
            tuple[str | ColumnElement] | list[str | ColumnElement] | str | ColumnElement
        ] = None,
        limit: Optional[int] = None,
    ) -> Sequence[Optional[DBUser]]:
        self._stmt = select(DBUser).where(
            or_(DBUser.is_active == is_active, is_active is None)
        )

        self.load(load)
        self.order_by(order_by)
        self.limit(limit)

        results: ScalarResult = await self._session.scalars(self._stmt)
        return results.unique().all()
