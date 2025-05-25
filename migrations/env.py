import asyncio

from alembic import context
from alembic.config import Config
from sqlalchemy import MetaData, URL
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from bot.configs.app import PostgresConfig
from bot.database.models import Base

config: Config = context.config
target_metadata: MetaData = Base.metadata


def _get_postgres_dsn() -> URL:
    _config: PostgresConfig = PostgresConfig()
    return _config.dsn.unicode_string()


def run_migrations_offline() -> None:
    context.configure(
        url=_get_postgres_dsn(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable: AsyncEngine = create_async_engine(url=_get_postgres_dsn())

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
