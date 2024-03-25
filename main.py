import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from src.app_config import AppConfig
from src.factory import create_bot, create_dispatcher
from src.runners import run_polling, run_webhook
from src.utils.logger import setup_logger


async def main() -> None:
    setup_logger()
    config: AppConfig = AppConfig.create()
    dp: Dispatcher = create_dispatcher(config=config)
    bot: Bot = create_bot(config=config, parse_mode=ParseMode.HTML)
    if config.webhook.use:
        return run_webhook(dp=dp, bot=bot, config=config)
    return await run_polling(dp=dp, bot=bot)


if __name__ == '__main__':
    asyncio.run(main())
