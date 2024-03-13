from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import Bot, Dispatcher, loggers
from aiogram.webhook import aiohttp_server as server
from aiogram_dialog import setup_dialogs
from aiohttp import web

from src.utils.loggers import MultilineLogger

if TYPE_CHECKING:
    from .app_config import AppConfig


async def polling_startup(dispatcher: Dispatcher, bot: Bot, config: AppConfig) -> None:
    await bot.delete_webhook(drop_pending_updates=config.common.drop_pending_updates)
    if config.common.drop_pending_updates:
        loggers.dispatcher.info("Updates skipped successfully")
    bg_manager_factory = setup_dialogs(dispatcher)
    dispatcher['bg_manager_factory'] = bg_manager_factory


async def webhook_startup(dispatcher: Dispatcher, bot: Bot, config: AppConfig) -> None:
    url: str = config.webhook.build_url()
    if await bot.set_webhook(
        url=url,
        allowed_updates=dispatcher.resolve_used_update_types(),
        secret_token=config.webhook.secret_token.get_secret_value(),
        drop_pending_updates=config.common.drop_pending_updates,
    ):
        return loggers.webhook.info("Main bot webhook successfully set on url '%s'", url)
    return loggers.webhook.error("Failed to set main bot webhook on url '%s'", url)


async def webhook_shutdown(bot: Bot, config: AppConfig) -> None:
    if not config.webhook.reset:
        return
    if await bot.delete_webhook():
        loggers.webhook.info("Dropped main bot webhook.")
    else:
        loggers.webhook.error("Failed to drop main bot webhook.")
    await bot.session.close()


async def run_polling(dp: Dispatcher, bot: Bot) -> None:
    dp.startup.register(polling_startup)
    return await dp.start_polling(bot)


def run_webhook(dp: Dispatcher, bot: Bot, config: AppConfig) -> None:
    app: web.Application = web.Application()
    server.SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=config.webhook.secret_token.get_secret_value(),
    ).register(app, path=config.webhook.path)
    server.setup_application(app, dp, bot=bot)
    app.update(**dp.workflow_data, bot=bot)
    dp.startup.register(webhook_startup)
    dp.shutdown.register(webhook_shutdown)

    return web.run_app(
        app=app,
        host=config.webhook.host,
        port=config.webhook.port,
        print=MultilineLogger(),
    )