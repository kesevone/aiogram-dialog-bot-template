from aiogram import Router

from . import handlers
from .dialogs import start_dialog

router = Router(name=__name__)
router.include_routers(handlers.router, start_dialog)
