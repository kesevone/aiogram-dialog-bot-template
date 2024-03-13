from typing import Final

from aiogram import Router

from . import pm

router = Router(name=__name__)
router.include_routers(pm.router)