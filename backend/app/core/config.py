from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_name: str = "MedMind Backend"
    version: str = "0.1.0"
    api_prefix: str = "/api"

    database_url: str = "postgresql+psycopg2://user:password@localhost:5432/medmind"
    redis_url: str = "redis://localhost:6379/0"
    cors_origins: List[str] = ["*"]

    access_token_expire_minutes: int = 60 * 24
    secret_key: str = "changeme"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
