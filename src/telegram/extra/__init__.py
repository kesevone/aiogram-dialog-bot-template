from aiogram import Router

from . import pm_banned

router = Router(name=__name__)
router.include_routers(pm_banned.router)
