from typing import Final

from aiogram import Router

from . import handlers
from .dialogs import main_dialog

router = Router(name=__name__)
router.include_routers(handlers.router, main_dialog)