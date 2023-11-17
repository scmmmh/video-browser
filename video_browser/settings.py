"""Access to the application settings."""
from pydantic import PostgresDsn, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings model."""

    dsn: PostgresDsn
    dev: bool = False
    video_base_url: HttpUrl

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
