from __future__ import annotations

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import SimpleEventIsolation
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram_dialog import setup_dialogs
from redis.asyncio import Redis

from src.app_config import AppConfig
from src.telegram import extra
from src.telegram.dialogs import common, user
from src.telegram.middlewares import DBSessionMiddleware, UserMiddleware
from src.utils import msgspec_json as mjson


def _setup_outer_middlewares(dp: Dispatcher, config: AppConfig) -> None:
    pool = dp["session_pool"] = config.postgres.build_pool(
        enable_logging=config.common.sqlalchemy_logging
    )

    dp.update.outer_middleware(DBSessionMiddleware(session_pool=pool))
    dp.update.outer_middleware(UserMiddleware())


def _setup_inner_middlewares(dp: Dispatcher) -> None:
    dp.callback_query.middleware(CallbackAnswerMiddleware())


def create_dispatcher(config: AppConfig) -> Dispatcher:
    redis: Redis = config.redis.build_client()

    dp: Dispatcher = Dispatcher(
        name="dispatcher",
        storage=RedisStorage(
            redis=redis,
            json_loads=mjson.decode,
            json_dumps=mjson.encode,
            key_builder=DefaultKeyBuilder(with_destiny=True, with_bot_id=True),
        ),
        redis=redis,
        config=config,
        events_isolation=SimpleEventIsolation(),
    )

    bg_manager_factory = setup_dialogs(router=dp)
    dp["bg_manager_factory"] = bg_manager_factory

    dp.include_routers(extra.router, common.router, user.router)
    _setup_outer_middlewares(dp=dp, config=config)
    _setup_inner_middlewares(dp=dp)
    return dp
