from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Database (Neon PostgreSQL)
    MYSQL_DB_HOST:          str = "ep-quiet-thunder-a4hp2h7b.us-east-1.aws.neon.tech"
    MYSQL_DB_PORT:          int = 5432
    MYSQL_DB_USER_NAME:     str = "neondb_owner"
    MYSQL_DB_USER_PASSWORD: str = "npg_j7aVLnXq4SiU"
    MYSQL_DB_NAME:          str = "neondb"

    def auth_db_params(self) -> tuple:
        return (
            self.MYSQL_DB_USER_NAME,
            self.MYSQL_DB_USER_PASSWORD,
            self.MYSQL_DB_HOST,
            self.MYSQL_DB_NAME,
            self.MYSQL_DB_PORT,
        )

    # JWT
    JWT_SECRET_KEY:              str  = "change-me-in-production"
    JWT_ALGORITHM:               str  = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int  = 30
    REFRESH_TOKEN_EXPIRE_DAYS:   int  = 7

    # App
    APP_TITLE:   str  = "Auth Service"
    APP_VERSION: str  = "1.0.0"
    APP_HOST:    str  = "0.0.0.0"
    APP_PORT:    int  = 8000
    DEBUG:       bool = False

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE:     int = 100


settings = Settings()