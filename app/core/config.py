from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "IssueFlow Lite"
    app_env: str = "development"
    debug: bool = False
    database_url: str = "postgresql+psycopg://issueflow:issueflow@localhost:5432/issueflow"
    secret_key: str = "development-only-change-me"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
