from __future__ import annotations

from typing import Sequence

from openai import AsyncOpenAI

from app.ai.config import LLMRuntimeConfig
from app.ai.providers.base import BaseChatModel, ChatMessage, LLMResult


class OpenAIChat(BaseChatModel):
    """OpenAI or OpenAI-compatible (vLLM/TGI) chat endpoint."""

    def __init__(self, config: LLMRuntimeConfig) -> None:
        super().__init__(config)
        client_kwargs: dict[str, str] = {}
        if config.api_key:
            client_kwargs["api_key"] = config.api_key
        if config.base_url:
            client_kwargs["base_url"] = config.base_url.rstrip("/")
        headers: dict[str, str] = {}
        # OpenRouter requires Referer + X-Title to whitelist the request origin.
        referer = getattr(config, "client_referer", None)
        title = getattr(config, "client_title", None)
        if referer:
            headers["HTTP-Referer"] = referer
            headers["Referer"] = referer
        if title:
            headers["X-Title"] = title
        self.client = AsyncOpenAI(default_headers=headers or None, **client_kwargs)

    def _provider_name(self) -> str:
        if self.config.base_url and "openai" not in self.config.base_url:
            return "openai-compatible"
        return "openai"

    async def generate(self, messages: Sequence[ChatMessage], **kwargs) -> LLMResult:
        completion = await self.client.chat.completions.create(
            model=self.config.model,
            messages=[m.__dict__ for m in messages],
            temperature=kwargs.get("temperature", 0.4),
            top_p=kwargs.get("top_p", 0.9),
            max_tokens=kwargs.get("max_tokens") or self.config.max_output_tokens,
            timeout=kwargs.get("timeout") or self.config.request_timeout,
        )
        choice = completion.choices[0].message
        content = choice.content or ""
        return LLMResult(
            content=content,
            model=self.config.model,
            provider=self._provider_name(),
            raw=completion.model_dump(),
        )

    async def aclose(self) -> None:
        await self.client.close()
