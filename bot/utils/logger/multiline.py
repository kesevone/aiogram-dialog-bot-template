import logging
from typing import Iterable, Optional


class MultilineLogger:
    level: int
    logger: logging.Logger

    __slots__ = ("level", "logger")

    def __init__(
        self,
        level: Optional[int] = logging.INFO,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self.level = level
        self.logger = logger or logging.getLogger()

    def __call__(self, messages: Iterable[str]) -> None:
        if isinstance(messages, str):
            messages = messages.splitlines()
        for msg in messages:
            self.logger.log(level=self.level, msg=msg)
