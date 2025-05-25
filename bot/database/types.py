from typing import Any, TypeAlias, Union

from sqlalchemy import ColumnElement
from sqlalchemy.orm import QueryableAttribute

LoadOption: TypeAlias = Union[
    QueryableAttribute[Any],
    list[QueryableAttribute[Any]],
    tuple[QueryableAttribute[Any], ...],
]

OrderByOption: TypeAlias = Union[
    str,
    ColumnElement,
    list[Union[str, ColumnElement]],
    tuple[Union[str, ColumnElement], ...],
]
