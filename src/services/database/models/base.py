from datetime import datetime
from typing import Annotated, TypeAlias

from sqlalchemy import BigInteger, DateTime, Integer, func, String
from sqlalchemy.dialects.postgresql import JSON, ARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, registry

from src.enums import IDTagEnum
from src.utils.generators import generate_id

Int16: TypeAlias = Annotated[int, 16]
Int64: TypeAlias = Annotated[int, 64]
Str256: TypeAlias = Annotated[str, 256]

UserIDStrKP = Annotated[str, mapped_column(
    String, primary_key=True, default=lambda _: generate_id(tag=IDTagEnum.USER)
)]

class Base(DeclarativeBase):
    registry = registry(
        type_annotation_map={
            Int16: Integer,
            Int64: BigInteger,
            Str256: String(256),
            dict: JSON,
            list: ARRAY(String),
            datetime: DateTime()
        }
    )

class TimeStampMixin:
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=datetime.now())