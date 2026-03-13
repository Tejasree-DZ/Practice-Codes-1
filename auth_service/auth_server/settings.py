"""
settings.py
-----------
Central configuration for the auth service.
 
All values can be overridden via environment variables or a .env file.
Pydantic-settings reads them automatically — no manual os.getenv() calls
needed anywhere in the codebase.
 
Priority order (highest → lowest):
    1. Actual environment variables  (export AUTH_DB_URL=...)
    2. Values in .env file
    3. Defaults defined here
 
Usage
-----
::
 
    from auth.auth_server.settings import settings
 
    print(settings.AUTH_DB_URL)
    print(settings.JWT_SECRET_KEY)
"""
 
from pydantic import BaseSettings, SettingsConfigDict
 
 
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",          # load from .env if present
        env_file_encoding="utf-8",
        extra="ignore",           # silently ignore unknown env vars
    )
 
    # ── Database (Neon PostgreSQL) ───────────────────────────────────────────
    # Full psycopg2 connection URL.
    # sslmode=require and channel_binding=require are mandatory for Neon.
    # Override via AUTH_DB_URL environment variable in production.
    AUTH_DB_URL: str = (
        "postgresql+psycopg2://neondb_owner:npg_j7aVLnXq4SiU"
        "@ep-quiet-thunder-a4hp2h7b.us-east-1.aws.neon.tech"
        "/neondb?sslmode=require&channel_binding=require"
    )
 
    # ── JWT ──────────────────────────────────────────────────────────────────
    # IMPORTANT: Override JWT_SECRET_KEY with a strong random secret in
    # production. Never commit the real secret to source control.
    # Generate one with:  openssl rand -hex 32
    JWT_SECRET_KEY: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30    # access token valid for 30 min
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7       # refresh token valid for 7 days
 
    # ── Application ──────────────────────────────────────────────────────────
    APP_TITLE: str = "Auth Service"
    APP_VERSION: str = "1.0.0"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    DEBUG: bool = False                      # set True to enable SQL echo + debug logs
 
    # ── CORS ─────────────────────────────────────────────────────────────────
    # Comma-separated list of allowed origins.
    # Override via CORS_ORIGINS env var, e.g:
    #   CORS_ORIGINS="http://localhost:3000,https://yourdomain.com"
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]
 
    # ── Pagination defaults ───────────────────────────────────────────────────
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
 
 
# ── Module-level singleton ────────────────────────────────────────────────────
# Import this everywhere — never instantiate Settings() directly.
#
#   from auth.auth_server.settings import settings
#
settings = Settings()