from __future__ import annotations

from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession
from sulguk import SULGUK_PARSE_MODE, AiogramSulgukMiddleware

from src.app_config import AppConfig
from src.utils import msgspec_json as mjson


def create_bot(config: AppConfig) -> Bot:
    """
    :return: Configured ``Bot``
    """
    session: AiohttpSession = AiohttpSession(
        json_loads=mjson.decode,
        json_dumps=mjson.encode
    )

    bot = Bot(
        token=config.common.bot_token.get_secret_value(),
        parse_mode=SULGUK_PARSE_MODE,
        session=session,
    )
    bot.session.middleware(AiogramSulgukMiddleware())
    return bot