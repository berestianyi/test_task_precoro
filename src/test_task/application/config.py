from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator


class Settings(BaseSettings):

    PROJECT_NAME: str = "test_task_precoro"
    DEBUG: bool = True
    ENV: str = "development"
    WTF_CSRF_ENABLED: bool = True
    TEMPLATES_AUTO_RELOAD: bool = True
    SECRET_KEY: str = "SECRET_KEY"

    DATABASE_DSN: str | None = None

    DB_NAME: str = "test_task_db"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_HOST: str = "db"
    DB_PORT: int = 5432

    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_URL: str = "redis://redis:6379/0"
    CELERY_BROKER_URL: str = "redis://redis:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/2"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

    @model_validator(mode="after")
    def _build_dsn(self):
        if not self.DATABASE_DSN:
            self.DATABASE_DSN = (
                f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}"
                f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            )
        return self

settings = Settings()