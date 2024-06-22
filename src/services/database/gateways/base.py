from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING

from sqlalchemy import ColumnElement, Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, QueryableAttribute

if TYPE_CHECKING:
    from src.services.database import Base


class BaseGateway:
    _session: AsyncSession
    _stmt: Optional[Select[Any]]

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._stmt = None

    def add(self, *instances: "Base") -> None:
        self._session.add_all(instances)

    async def delete(self, *instances: "Base") -> None:
        for instance in instances:
            await self._session.delete(instance)

    async def commit(self, *instances: "Base") -> None:
        for instance in instances:
            self.add(instance)

        await self._session.commit()

    def load(
        self,
        relations: Optional[
            tuple[QueryableAttribute[Any]]
            | list[QueryableAttribute[Any]]
            | QueryableAttribute[Any]
        ] = None,
    ) -> None:
        if not relations:
            return

        if not isinstance(relations, (list, tuple)):
            relations = [relations]

        self._stmt = self._stmt.options(
            *[joinedload(relation) for relation in relations]
        )

    def order_by(
        self,
        columns: Optional[
            tuple[str | ColumnElement] | list[str | ColumnElement] | str | ColumnElement
        ] = None,
    ) -> None:
        if not columns:
            return

        if not isinstance(columns, (list, tuple)):
            columns = [columns]

        self._stmt = self._stmt.order_by(*columns)

    def limit(self, limit: Optional[int] = None) -> None:
        if not limit:
            return

        self._stmt = self._stmt.limit(limit=limit)
