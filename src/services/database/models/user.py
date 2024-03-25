from __future__ import annotations

from typing import Optional

from aiogram.types import User
from aiogram.utils.link import create_tg_link
from sqlalchemy.orm import Mapped

from .base import Base, Int64, TimeStampMixin, UserIDStrKP


class DBUser(Base, TimeStampMixin):
    __tablename__ = 'users'

    id: Mapped[UserIDStrKP]
    telegram_id: Mapped[Int64]
    name: Mapped[Optional[str]]

    @property
    def url(self) -> str:
        return create_tg_link('user', id=self.id)

    @classmethod
    def create(cls, user: User) -> DBUser:
        return DBUser(
            telegram_id=user.id,
            name=user.full_name
        )