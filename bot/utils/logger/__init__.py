import logging

from .setup import setup_logger
from .multiline import MultilineLogger

__all__ = ["database", "service", "scheduler_logger", "setup_logger", "MultilineLogger"]

database: logging.Logger = logging.getLogger("bot.database")
service: logging.Logger = logging.getLogger("bot.service")
scheduler_logger: logging.Logger = logging.getLogger("bot.scheduler")
