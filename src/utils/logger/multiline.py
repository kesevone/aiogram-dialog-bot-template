from logging import INFO, Logger, getLogger
from typing import Iterable, Optional


class MultilineLogger:
    level: int
    logger: Logger

    __slots__ = ("level", "logger")

    def __init__(self, level: int = INFO, logger: Optional[Logger] = None) -> None:
        self.level = level
        self.logger = logger or getLogger()

    def __call__(self, messages: Iterable[str]) -> None:
        if isinstance(messages, str):
            messages = messages.splitlines()
        for msg in messages:
            self.logger.log(level=self.level, msg=msg)
