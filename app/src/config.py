from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "DevOps Performance Platform"
    app_env: str = "development"

    database_host: str = "localhost"
    database_port: int = 5432
    database_name: str = "performance_db"
    database_user: str = "app_user"
    database_password: str = "app_password"

    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg://"
            f"{self.database_user}:{self.database_password}"
            f"@{self.database_host}:{self.database_port}"
            f"/{self.database_name}"
        )

    @property
    def redis_url(self) -> str:
        if self.redis_password:
            return (
                f"redis://:{self.redis_password}"
                f"@{self.redis_host}:{self.redis_port}/0"
            )

        return f"redis://{self.redis_host}:{self.redis_port}/0"


settings = Settings()
