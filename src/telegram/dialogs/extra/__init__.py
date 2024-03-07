from typing import Final

from aiogram import Router

from . import pm

router: Final[Router] = Router(name=__name__)
router.include_routers(pm.router)