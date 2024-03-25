from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseRepository
from .users import UsersRepository


class Repository(BaseRepository):
    """
    The general repository.
    """

    user: UsersRepository

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session)
        self.user = UsersRepository(session=session)