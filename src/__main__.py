import asyncio

from aiogram import Bot, Dispatcher

from .app_config import AppConfig
from .factory import create_app_config, create_bot, create_dispatcher
from .runners import run_polling, run_webhook
from .utils.loggers import setup_logger


async def main() -> None:
    setup_logger()
    config: AppConfig = create_app_config()
    dp: Dispatcher = create_dispatcher(config=config)
    bot: Bot = create_bot(config=config)
    if config.webhook.use:
        return run_webhook(dp=dp, bot=bot, config=config)
    return await run_polling(dp=dp, bot=bot)


if __name__ == "__main__":
    asyncio.run(main())
