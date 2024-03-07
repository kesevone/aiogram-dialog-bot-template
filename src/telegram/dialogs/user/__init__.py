from typing import Final

from aiogram import Router

from . import handlers
from .dialogs import start_dialog

router: Final[Router] = Router(name=__name__)
router.include_routers(handlers.router, start_dialog)