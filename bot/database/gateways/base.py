from __future__ import annotations

from typing import Any, Iterable, Optional, TYPE_CHECKING

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from bot.database.types import LoadOption, OrderByOption
from bot.utils.database.normalize_iterable import normalize_iterable

if TYPE_CHECKING:
    from bot.database import Base


class BaseGateway:
    _session: AsyncSession
    _stmt: Optional[Select[Any]]

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._stmt = None

    def add(self, *instances: "Base") -> None:
        self._session.add_all(instances)

    async def flush(self, *instances: "Base") -> None:
        await self._session.flush(instances)

    async def delete(self, *instances: "Base") -> None:
        for instance in instances:
            await self._session.delete(instance)

    async def commit(self) -> None:
        await self._session.commit()

    def _load(
        self,
        values: Optional[LoadOption] = None,
    ) -> None:
        relations: Iterable = normalize_iterable(values)
        if relations:
            self._stmt = self._stmt.options(
                *[joinedload(relation) for relation in relations]
            )

    def _order_by(
        self,
        values: Optional[OrderByOption] = None,
    ) -> None:
        criteria: Iterable = normalize_iterable(values)
        if criteria:
            self._stmt = self._stmt.order_by(*criteria)

    def _limit(self, limit: Optional[int] = None) -> None:
        if not limit:
            return

        self._stmt = self._stmt.limit(limit=limit)
