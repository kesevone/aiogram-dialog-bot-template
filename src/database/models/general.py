from __future__ import annotations

from typing import Optional, Self

from aiogram import html
from aiogram.types import User
from aiogram.utils.link import create_tg_link
from sqlalchemy import true
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, IntPK, TimeStampMixin


class DBUser(Base, TimeStampMixin):
    __tablename__ = "users"

    id: Mapped[IntPK]
    full_name: Mapped[str]
    username: Mapped[Optional[str]]
    is_active: Mapped[bool] = mapped_column(server_default=true())

    @property
    def url(self) -> str:
        return create_tg_link("user", id=self.id)

    @property
    def mention(self) -> str:
        return html.link(value=self.full_name, link=self.url)

    @classmethod
    def from_any(
        cls,
        user_id: int,
        full_name: Optional[str] = None,
        username: Optional[str] = None,
        is_active: Optional[bool] = None,
    ) -> Self:
        return cls(
            id=user_id, full_name=full_name, username=username, is_active=is_active
        )

    @classmethod
    def from_aiogram(cls, user: User, is_active: Optional[bool] = None) -> Self:
        return cls(
            id=user.id,
            full_name=user.full_name,
            username=user.username,
            is_active=is_active,
        )
