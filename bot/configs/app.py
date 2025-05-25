from __future__ import annotations

from secrets import token_urlsafe
from typing import Optional, Self

from aiogram.client.telegram import TelegramAPIServer
from apscheduler.datastores.sqlalchemy import SQLAlchemyDataStore
from pydantic import BaseModel, Field, PostgresDsn, RedisDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from redis.asyncio import Redis
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)

from bot.scheduler import CustomScheduler


class _BaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore", env_file=".env", env_file_encoding="utf-8"
    )


class CommonConfig(_BaseSettings, env_prefix="COMMON_"):
    bot_token: SecretStr
    admin_id: int
    drop_pending_updates: bool
    sqlalchemy_logging: bool


class LocalBotAPI(_BaseSettings, env_prefix="LOCALBOTAPI_"):
    enabled: bool
    base_url: str
    file_url: str
    is_local: bool

    def build_server(self) -> TelegramAPIServer:
        if not self.file_url:
            return TelegramAPIServer.from_base(self.base_url, is_local=self.is_local)

        base_url: str = self.base_url.rstrip("/")
        return TelegramAPIServer(
            base=base_url, file=self.file_url, is_local=self.is_local
        )


class PostgresConfig(_BaseSettings, env_prefix="POSTGRES_"):
    dsn: PostgresDsn

    def build_pool(
        self, dsn: Optional[str | URL] = None, enable_logging: bool = False
    ) -> async_sessionmaker[AsyncSession]:
        if dsn is None:
            dsn = self.dsn.unicode_string()
        engine: AsyncEngine = create_async_engine(
            url=dsn,
            echo=enable_logging,
            pool_size=20,
            max_overflow=10,
            pool_timeout=30,
            connect_args={"command_timeout": 30},
        )
        return async_sessionmaker(engine, expire_on_commit=False)


class SchedulerConfig(_BaseSettings, env_prefix="SCHEDULER_"):
    enabled: bool
    logging: bool
    dsn: str

    def build_engine(
        self, dsn: Optional[str | URL] = None, enable_logging: bool = False
    ) -> AsyncEngine:
        if dsn is None:
            dsn = self.dsn
        engine: AsyncEngine = create_async_engine(url=dsn, echo=enable_logging)
        return engine

    def build_pool(
        self, dsn: Optional[str | URL] = None, enable_logging: bool = False
    ) -> tuple[async_sessionmaker[AsyncSession], AsyncEngine]:
        engine: AsyncEngine = self.build_engine(dsn=dsn, enable_logging=enable_logging)
        return async_sessionmaker(engine, expire_on_commit=False), engine

    def build_scheduler(self, engine: AsyncEngine) -> CustomScheduler:
        return CustomScheduler(
            data_store=SQLAlchemyDataStore(engine_or_url=engine),
            enable_logging=self.logging,
        )


class RedisConfig(_BaseSettings, env_prefix="REDIS_"):
    enabled: bool
    dsn: RedisDsn

    def build_client(self) -> Redis:
        return Redis.from_url(self.dsn.unicode_string())


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
    localbotapi: LocalBotAPI
    postgres: PostgresConfig
    scheduler: SchedulerConfig
    redis: RedisConfig
    webhook: WebhookConfig

    @classmethod
    def create(cls) -> Self:
        return cls(
            common=CommonConfig(),
            localbotapi=LocalBotAPI(),
            postgres=PostgresConfig(),
            scheduler=SchedulerConfig(),
            redis=RedisConfig(),
            webhook=WebhookConfig(),
        )
