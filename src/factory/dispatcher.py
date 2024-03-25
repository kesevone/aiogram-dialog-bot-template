from __future__ import annotations

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import SimpleEventIsolation
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from redis.asyncio import Redis

from src.app_config import AppConfig
from src.middlewares import DBSessionMiddleware, UserMiddleware
from src.services.database import create_pool
from src.telegram.dialogs import user
from src.utils import msgspec_json as mjson


def _setup_outer_middlewares(dp: Dispatcher, config: AppConfig) -> None:
    pool = dp['session_pool'] = create_pool(
        dsn=config.postgres.build_dsn(),
        enable_logging=config.common.sqlalchemy_logging
    )

    dp.update.outer_middleware(DBSessionMiddleware(session_pool=pool))
    dp.update.outer_middleware(UserMiddleware())

def _setup_inner_middlewares(dp: Dispatcher) -> None:
    dp.callback_query.middleware(CallbackAnswerMiddleware())

def create_dispatcher(config: AppConfig) -> Dispatcher:
    """
    :return: Configured ``Dispatcher`` with installed middlewares and included routers
    """
    redis: Redis = config.redis.build_client()

    jobstores = {
        'redis': RedisJobStore(
            db=config.redis.db,
            host=config.redis.host,
            port=config.redis.port
        )
    }
    scheduler = AsyncIOScheduler()
    scheduler.add_jobstore(jobstores['redis'], 'redis')

    dp: Dispatcher = Dispatcher(
        name='main_dispatcher',
        storage=RedisStorage(
            redis=redis,
            json_loads=mjson.decode,
            json_dumps=mjson.encode,
            key_builder=DefaultKeyBuilder(with_destiny=True)
        ),
        redis=redis,
        config=config,
        events_isolation=SimpleEventIsolation()
    )
    dp.include_routers(
        user.router
    )
    _setup_outer_middlewares(dp=dp, config=config)
    _setup_inner_middlewares(dp=dp)
    return dp
