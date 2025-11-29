from functools import lru_cache
from typing import List

from pydantic import AliasChoices, Field
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

    ai_provider: str = "openai"
    ai_model: str = "gpt-4o-mini"
    ai_base_url: str | None = Field(
        default=None,
        validation_alias=AliasChoices("AI_BASE_URL", "OPENAI_BASE_URL", "openai_base_url"),
    )
    ai_api_key: str | None = Field(
        default=None,
        validation_alias=AliasChoices("AI_API_KEY", "OPENAI_API_KEY", "openai_api_key"),
    )
    ai_request_timeout_seconds: int = 30
    ai_max_output_tokens: int | None = None
    ai_client_referer: str | None = Field(default="http://localhost:3000", validation_alias="AI_CLIENT_REFERER")
    ai_client_title: str | None = Field(default="MedMind Portal", validation_alias="AI_CLIENT_TITLE")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
