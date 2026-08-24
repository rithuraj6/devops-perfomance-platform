from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "DevOps Performance Platform"
    app_env: str = "development"

    database_url: str = (
        "postgresql+psycopg://app_user:app_password"
        "@localhost:5432/performance_db"
    )

    redis_url: str = "redis://localhost:6379/0"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
