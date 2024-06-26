from __future__ import annotations

from typing import TYPE_CHECKING

import aiogram_fastapi_server as server
import uvicorn
from aiogram import Bot, Dispatcher, loggers
from fastapi import FastAPI

from .data import LOGGING_CONFIG

if TYPE_CHECKING:
    from .app_config import AppConfig


async def polling_startup(bot: Bot, config: AppConfig) -> None:
    await bot.delete_webhook(drop_pending_updates=config.common.drop_pending_updates)

    if config.common.drop_pending_updates:
        return loggers.dispatcher.info("Pending updates successfully dropped.")


async def webhook_startup(dispatcher: Dispatcher, bot: Bot, config: AppConfig) -> None:
    url: str = config.webhook.build_url()
    if await bot.set_webhook(
        url=url,
        allowed_updates=dispatcher.resolve_used_update_types(),
        secret_token=config.webhook.secret_token.get_secret_value(),
        drop_pending_updates=config.common.drop_pending_updates,
    ):
        return loggers.webhook.info("Bot webhook successfully set on %s", url)
    return loggers.webhook.error("Failed to set bot webhook on %s", url)


async def webhook_shutdown(bot: Bot, config: AppConfig) -> None:
    if not config.webhook.reset:
        return

    if await bot.delete_webhook():
        loggers.webhook.info("Dropped bot webhook.")
    else:
        loggers.webhook.error("Failed to drop bot webhook.")
    return await bot.session.close()


def run_bot(dp: Dispatcher, bot: Bot, config: AppConfig) -> None:
    if config.webhook.use:
        return run_webhook(dp=dp, bot=bot, config=config)
    return run_polling(dp=dp, bot=bot)


def run_polling(dp: Dispatcher, bot: Bot) -> None:
    dp.startup.register(polling_startup)
    return dp.run_polling(bot)


def run_webhook(dp: Dispatcher, bot: Bot, config: AppConfig) -> None:
    app: FastAPI = FastAPI()
    server.SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=config.webhook.secret_token.get_secret_value(),
    ).register(app, path=config.webhook.path)
    server.setup_application(app, dp, bot=bot)

    dp.startup.register(webhook_startup)
    dp.shutdown.register(webhook_shutdown)
    return uvicorn.run(
        app=app,
        host=config.webhook.host,
        port=config.webhook.port,
        log_config=LOGGING_CONFIG,
    )
