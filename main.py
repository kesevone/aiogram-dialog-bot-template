from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from src.app_config import AppConfig
from src.factory import create_bot, create_dispatcher
from src.runners import run_bot
from src.utils.logger.setup import setup_logger


def main() -> None:
    setup_logger()
    config: AppConfig = AppConfig.create()
    dp: Dispatcher = create_dispatcher(config=config)
    bot: Bot = create_bot(config=config, parse_mode=ParseMode.HTML)
    return run_bot(dp=dp, bot=bot, config=config)


if __name__ == "__main__":
    main()
