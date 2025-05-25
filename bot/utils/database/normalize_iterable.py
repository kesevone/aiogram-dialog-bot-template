from typing import Iterable, Optional

from bot.database.types import LoadOption, OrderByOption


def normalize_iterable(value: Optional[LoadOption | OrderByOption] = None) -> Iterable:
    if value is None:
        return []
    if not isinstance(value, Iterable) or isinstance(value, (str, bytes)):
        return [value]
    return value
