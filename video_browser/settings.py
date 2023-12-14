"""Access to the application settings."""
import os

from pydantic import PostgresDsn, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings model."""

    dsn: PostgresDsn
    dev: bool = False
    video_base_url: HttpUrl
    data_base_path: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


if 'ALEMBIC' not in os.environ:
    settings = Settings()
else:
    settings = None
