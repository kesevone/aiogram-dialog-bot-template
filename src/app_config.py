from __future__ import annotations
from secrets import token_urlsafe

from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict
from redis.asyncio import ConnectionPool, Redis
from sqlalchemy import URL


class _BaseSettings(BaseSettings):
    model_config = SettingsConfigDict(extra='ignore', env_file='.env', env_file_encoding='utf-8')

class CommonConfig(_BaseSettings, env_prefix='COMMON_'):
    bot_token: SecretStr
    drop_pending_updates: bool
    sqlalchemy_logging: bool
    admin_id: int

class PostgresConfig(_BaseSettings, env_prefix='POSTGRES_'):
    host: str
    db: str
    password: SecretStr
    port: int
    user: str

    def build_dsn(self) -> URL:
        return URL.create(
            drivername='postgresql+asyncpg',
            username=self.user,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            database=self.db,
        )

class RedisConfig(_BaseSettings, env_prefix='REDIS_'):
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

class WebhookConfig(_BaseSettings, env_prefix='WEBHOOK_'):
    use: bool
    reset: bool
    base_url: str
    path: str
    port: int
    host: str
    secret_token: SecretStr = Field(default_factory=token_urlsafe)

    def build_url(self) -> str:
        return f'{self.base_url}{self.path}'

class AppConfig(BaseModel):
    common: CommonConfig
    postgres: PostgresConfig
    redis: RedisConfig
    webhook: WebhookConfig

    @staticmethod
    def create() -> AppConfig:
        return AppConfig(
            common=CommonConfig(),
            postgres=PostgresConfig(),
            redis=RedisConfig(),
            webhook=WebhookConfig(),
        )
