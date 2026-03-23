from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Database (Neon PostgreSQL - Core Service DB)
    MYSQL_DB_HOST:          str = "ep-aged-sound-anyzwg5i-pooler.c-6.us-east-1.aws.neon.tech"
    MYSQL_DB_PORT:          int = 5432
    MYSQL_DB_USER_NAME:     str = "neondb_owner"
    MYSQL_DB_USER_PASSWORD: str = "npg_icfbaA3W5hRJ"
    MYSQL_DB_NAME:          str = "neondb"

    def core_db_params(self) -> tuple:
        return (
            self.MYSQL_DB_USER_NAME,
            self.MYSQL_DB_USER_PASSWORD,
            self.MYSQL_DB_HOST,
            self.MYSQL_DB_NAME,
            self.MYSQL_DB_PORT,
        )

    AUTH_SERVICE_URL:            str  = "http://localhost:8000"
    JWT_SECRET_KEY:              str  = "change-me-in-production"
    JWT_ALGORITHM:               str  = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int  = 30
    APP_TITLE:                   str  = "Core Service"
    APP_VERSION:                 str  = "1.0.0"
    APP_HOST:                    str  = "0.0.0.0"
    APP_PORT:                    int  = 8001
    DEBUG:                       bool = False
    CORS_ORIGINS:          list[str]  = ["http://localhost:3000"]
    DEFAULT_PAGE_SIZE:           int  = 20
    MAX_PAGE_SIZE:               int  = 100


settings = Settings()