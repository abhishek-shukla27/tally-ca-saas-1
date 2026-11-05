"""
config.py
~~~~~~~~~
Centralised settings loaded from environment variables (or a .env file).
Uses Pydantic v2 BaseSettings for type-safe configuration.
"""

from __future__ import annotations

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ── Database ─────────────────────────────────────────────────────────────
    DATABASE_URL: str = (
        "postgresql://postgres:postgres@localhost:5432/tally_ca_saas"
    )

    # ── App ──────────────────────────────────────────────────────────────────
    APP_TITLE: str = "Tally-CA SaaS Backend"
    APP_VERSION: str = "0.2.0"
    DEBUG: bool = False

    # ── Security ─────────────────────────────────────────────────────────────
    # Token length used when generating new client tokens (characters)
    CLIENT_TOKEN_LENGTH: int = 48

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def check_db_url(cls, v: str) -> str:
        if not v.startswith(("postgresql://", "postgresql+psycopg2://")):
            raise ValueError(
                "DATABASE_URL must start with 'postgresql://' or "
                "'postgresql+psycopg2://'"
            )
        return v


# Single shared instance imported everywhere
settings = Settings()

