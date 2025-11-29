from dataclasses import dataclass
from typing import Optional

from app.core.config import Settings, settings


@dataclass
class LLMRuntimeConfig:
    """Runtime configuration for selecting and tuning chat models."""

    provider: str
    model: str
    base_url: Optional[str]
    api_key: Optional[str]
    request_timeout: float
    max_output_tokens: Optional[int]
    client_referer: Optional[str]
    client_title: Optional[str]

    @classmethod
    def from_settings(cls, source: Settings | None = None) -> "LLMRuntimeConfig":
        conf = source or settings
        return cls(
            provider=conf.ai_provider,
            model=conf.ai_model,
            base_url=conf.ai_base_url,
            api_key=conf.ai_api_key,
            request_timeout=conf.ai_request_timeout_seconds,
            max_output_tokens=conf.ai_max_output_tokens,
            client_referer=getattr(conf, "ai_client_referer", None),
            client_title=getattr(conf, "ai_client_title", None),
        )
