from aiogram import F, Router
from aiogram.enums import ChatType

from . import exceptions

router = Router(name=__name__)
router.include_routers(exceptions.router)
router.message.filter(F.chat.type == ChatType.PRIVATE)
