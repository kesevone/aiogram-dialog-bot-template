from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseGateway
from .users import UsersGateway


class Gateway(BaseGateway):
    users: UsersGateway

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session)
        self.users = UsersGateway(session=session)
