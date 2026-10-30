"""Configuration module for the application."""

import json
from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        env_prefix="",
    )

    # Telegram Configuration
    telegram_api_id: int = Field(..., description="Telegram API ID from my.telegram.org")
    telegram_api_hash: str = Field(..., description="Telegram API Hash from my.telegram.org")
    telegram_bot_token: str = Field(..., description="Bot token from @BotFather")

    # Authorization / Access Control
    allowed_user_ids: list[int] = Field(
        default_factory=list,
        description="List of Telegram User IDs allowed to use the bot. If empty, access is open to all users.",
    )

    @field_validator("allowed_user_ids", mode="before")
    @classmethod
    def parse_allowed_user_ids(cls, v: Any) -> list[int]:
        """Parse comma-separated string, JSON array, or list of user IDs."""
        if isinstance(v, str):
            v = v.strip()
            if not v:
                return []
            if v.startswith("[") and v.endswith("]"):
                try:
                    parsed = json.loads(v)
                    if isinstance(parsed, list):
                        return [int(x) for x in parsed]
                except Exception:
                    pass
            return [int(x.strip()) for x in v.split(",") if x.strip()]
        elif isinstance(v, (list, tuple, set)):
            return [int(x) for x in v]
        elif isinstance(v, int):
            return [v]
        return []

    # Database Configuration
    database_url: str = Field(
        default="sqlite:///data/seedrccbot.sqlite",
        description="Database connection URL",
    )

    # Bot Settings
    bot_name: str = Field(default="Seedrcc Bot", description="Name of the bot")
    max_torrent_file_size: int = Field(
        default=1 * 1024 * 1024,  # 1 MB
        description="Maximum allowed size for torrent file uploads in bytes",
    )
    page_size: int = Field(default=8, description="Number of items to show per page in lists")

    # Monitoring
    sentry_dsn: str | None = Field(default=None, description="Sentry DSN for error monitoring")

    # Security
    encryption_key: str = Field(..., description="Fernet encryption key for securing credentials")


# Global settings instance
settings = Settings()
