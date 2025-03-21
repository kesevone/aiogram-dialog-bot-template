from __future__ import annotations

from typing import Optional

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from sulguk import AiogramSulgukMiddleware

from bot.configs.app import AppConfig
from bot.utils import msgspec_json as mjson


def create_bot(
    config: AppConfig, parse_mode: Optional[ParseMode] = ParseMode.HTML
) -> Bot:
    session: AiohttpSession = AiohttpSession(
        json_loads=mjson.decode, json_dumps=mjson.encode
    )
    if config.localbotapi.enabled:
        session.api = config.localbotapi.build_server()

    bot = Bot(
        token=config.common.bot_token.get_secret_value(),
        session=session,
        default=DefaultBotProperties(parse_mode=parse_mode),
    )
    bot.session.middleware(AiogramSulgukMiddleware())
    return bot
