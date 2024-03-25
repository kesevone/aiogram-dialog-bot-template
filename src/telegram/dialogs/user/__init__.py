from aiogram import Router

from . import main

router = Router(name=__name__)
router.include_routers(main.router)