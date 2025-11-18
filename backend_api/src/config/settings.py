from __future__ import annotations

import secrets
from functools import lru_cache
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    SECURITY
    - SECRET_KEY: Required for signing JWTs and encryption key derivation.
    - ACCESS_TOKEN_TTL: Seconds for access token lifetime.
    - REFRESH_TOKEN_TTL: Seconds for refresh token lifetime.
    - ENCRYPTION_MASTER_KEY: Base64 or 32+ length string used to derive encryption keys.

    DATABASE
    - DB_URL: SQLAlchemy database URL (e.g., sqlite+aiosqlite:///./app.db or postgresql+psycopg://...)

    INTEGRATIONS
    - EKYC_PROVIDER_API_KEY: API key for mock eKYC provider.
    - EKYC_WEBHOOK_SECRET: Secret to verify eKYC webhook signatures.

    OTHER
    - CORS_ORIGINS: Comma-separated list of allowed origins.
    - RATE_LIMITS: Not implemented at framework level here (placeholder).
    - LOG_LEVEL: Logging level (DEBUG/INFO/WARN/ERROR).
    - ENABLE_METRICS: "true"/"false" to toggle metrics (placeholder).
    """

    # Security
    SECRET_KEY: str = Field(default_factory=lambda: secrets.token_urlsafe(64), description="JWT signing secret")
    ACCESS_TOKEN_TTL: int = Field(default=900, description="Access token TTL seconds (default 15 min)")
    REFRESH_TOKEN_TTL: int = Field(default=2592000, description="Refresh token TTL seconds (default 30 days)")
    ENCRYPTION_MASTER_KEY: str = Field(default="", description="Master key for encryption")

    # Database
    DB_URL: str = Field(default="sqlite:///./app.db", description="SQLAlchemy DB URL")

    # Integrations
    EKYC_PROVIDER_API_KEY: str = Field(default="", description="Mock eKYC provider API key")
    EKYC_WEBHOOK_SECRET: str = Field(default="", description="Mock eKYC webhook secret")

    # Other
    CORS_ORIGINS: str = Field(default="*", description="CSV list of allowed CORS origins")
    RATE_LIMITS: str = Field(default="", description="Placeholder for rate limits")
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    ENABLE_METRICS: bool = Field(default=False, description="Toggle metrics")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @field_validator("ACCESS_TOKEN_TTL", "REFRESH_TOKEN_TTL")
    @classmethod
    def _validate_positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("TTL must be positive")
        return v

    @field_validator("SECRET_KEY")
    @classmethod
    def _validate_secret_key(cls, v: str) -> str:
        if not v or len(v) < 32:
            # ensure minimal strength; value may be auto-generated fallback
            return v if v and len(v) >= 32 else secrets.token_urlsafe(48)
        return v


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Returns cached settings instance.
    """
    return Settings()


# Singleton-like settings for convenience import
settings = get_settings()
