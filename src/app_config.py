from __future__ import annotations

from secrets import token_urlsafe
from typing import Optional, Self

from apscheduler.datastores.sqlalchemy import SQLAlchemyDataStore
from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from redis.asyncio import ConnectionPool, Redis
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)

from src.scheduler import CustomScheduler


class _BaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore", env_file=".env", env_file_encoding="utf-8"
    )


class CommonConfig(_BaseSettings, env_prefix="COMMON_"):
    bot_token: SecretStr
    admin_id: int
    drop_pending_updates: bool
    sqlalchemy_logging: bool


class PostgresConfig(_BaseSettings, env_prefix="POSTGRES_"):
    db: str
    host: str
    port: int
    user: str
    password: SecretStr

    def build_dsn(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.user,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            database=self.db,
        )

    def build_pool(
        self, dsn: Optional[str | URL] = None, enable_logging: bool = False
    ) -> async_sessionmaker[AsyncSession]:
        if dsn is None:
            dsn = self.build_dsn()
        engine: AsyncEngine = create_async_engine(url=dsn, echo=enable_logging)
        return async_sessionmaker(engine, expire_on_commit=False)


class SchedulerConfig(_BaseSettings, env_prefix="SCHEDULER_"):
    enabled: bool
    logging: bool
    db_path: str

    def build_dsn(self) -> URL:
        return URL.create(
            drivername="sqlite+aiosqlite",
            database=self.db_path,
        )

    def build_engine(
        self, dsn: Optional[str | URL] = None, enable_logging: bool = False
    ) -> AsyncEngine:
        if dsn is None:
            dsn = self.build_dsn()
        engine: AsyncEngine = create_async_engine(url=dsn, echo=enable_logging)
        return engine

    def build_pool(
        self, dsn: Optional[str | URL] = None, enable_logging: bool = False
    ) -> async_sessionmaker[AsyncSession] | AsyncEngine:
        engine: AsyncEngine = self.build_engine(dsn=dsn, enable_logging=enable_logging)
        return async_sessionmaker(engine, expire_on_commit=False), engine

    def build_scheduler(self, engine: AsyncEngine) -> CustomScheduler:
        return CustomScheduler(
            data_store=SQLAlchemyDataStore(engine_or_url=engine),
            enable_logging=self.logging,
        )


class RedisConfig(_BaseSettings, env_prefix="REDIS_"):
    host: str
    port: int
    db: int

    def build_client(self) -> Redis:
        return Redis(
            connection_pool=ConnectionPool(
                host=self.host,
                port=self.port,
                db=self.db,
            )
        )


class WebhookConfig(_BaseSettings, env_prefix="WEBHOOK_"):
    enabled: bool
    reset: bool
    base_url: str
    path: str
    port: int
    host: str
    secret_token: SecretStr = Field(default_factory=token_urlsafe)

    def build_url(self) -> str:
        return f"{self.base_url}{self.path}"


class AppConfig(BaseModel):
    common: CommonConfig
    postgres: PostgresConfig
    scheduler: SchedulerConfig
    redis: RedisConfig
    webhook: WebhookConfig

    @classmethod
    def create(cls) -> Self:
        return cls(
            common=CommonConfig(),
            postgres=PostgresConfig(),
            scheduler=SchedulerConfig(),
            redis=RedisConfig(),
            webhook=WebhookConfig(),
        )
