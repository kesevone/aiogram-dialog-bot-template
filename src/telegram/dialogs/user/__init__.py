from aiogram import F, Router
from aiogram.enums import ChatType

from . import main

router = Router(name=__name__)
router.include_routers(main.router)
router.message.filter(F.chat.type == ChatType.PRIVATE)
