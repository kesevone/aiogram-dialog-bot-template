from __future__ import annotations

from aiogram import Dispatcher
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage, SimpleEventIsolation
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from aiogram_dialog import setup_dialogs
from redis.asyncio import Redis

from bot.configs.app import AppConfig
from bot.telegram import extra
from bot.telegram.dialogs import common, user
from bot.telegram.middlewares import DBSessionMiddleware, UserMiddleware
from bot.utils import msgspec_json as mjson


def _setup_outer_middlewares(dp: Dispatcher, config: AppConfig) -> None:
    pool = dp["session_pool"] = config.postgres.build_pool(
        enable_logging=config.common.sqlalchemy_logging
    )

    dp.update.outer_middleware(DBSessionMiddleware(session_pool=pool))
    dp.update.outer_middleware(UserMiddleware())


def setup_storage(redis: Redis, config: AppConfig) -> BaseStorage:
    if config.redis.enabled:
        storage = RedisStorage(
            redis=redis,
            json_loads=mjson.decode,
            json_dumps=mjson.encode,
            key_builder=DefaultKeyBuilder(with_destiny=True, with_bot_id=True),
        )
    else:
        storage = MemoryStorage()

    return storage


def create_dispatcher(config: AppConfig) -> Dispatcher:
    redis: Redis = config.redis.build_client()
    storage: BaseStorage = setup_storage(redis=redis, config=config)
    dp: Dispatcher = Dispatcher(
        name="dispatcher",
        config=config,
        redis=redis,
        storage=storage,
        events_isolation=SimpleEventIsolation(),
    )

    bg_manager_factory = setup_dialogs(router=dp)
    dp["bg_manager_factory"] = bg_manager_factory

    dp.include_routers(extra.router, common.router, user.router)
    _setup_outer_middlewares(dp=dp, config=config)
    return dp
