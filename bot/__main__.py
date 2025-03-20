import asyncio

from aiogram import Bot, Dispatcher
from sqlalchemy.orm import close_all_sessions

from bot.configs.app import AppConfig
from bot.factory import create_bot, create_dispatcher
from bot.runners import run_bot
from bot.utils.logger.setup import setup_logger


async def main() -> None:
    setup_logger()
    config: AppConfig = AppConfig.create()
    dp: Dispatcher = create_dispatcher(config=config)
    bot: Bot = create_bot(config=config)
    return await run_bot(dp=dp, bot=bot, config=config)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        close_all_sessions()
