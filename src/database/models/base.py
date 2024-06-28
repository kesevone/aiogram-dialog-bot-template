from datetime import datetime, timezone
from typing import Annotated, TypeAlias

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, func, String
from sqlalchemy.dialects.postgresql import JSON, ARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, registry

Int16: TypeAlias = Annotated[int, 16]
Int64: TypeAlias = Annotated[int, 64]
Str256: TypeAlias = Annotated[str, 256]

IntPK = Annotated[int, mapped_column(BigInteger, primary_key=True)]
UserFK = Annotated[
    int, mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
]


class Base(DeclarativeBase):
    registry = registry(
        type_annotation_map={
            Int16: Integer,
            Int64: BigInteger,
            Str256: String(256),
            dict: JSON,
            list: ARRAY(String),
            datetime: DateTime(timezone=True),
        }
    )


class TimeStampMixin:
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=func.now(),
        server_default=func.now(),
    )
