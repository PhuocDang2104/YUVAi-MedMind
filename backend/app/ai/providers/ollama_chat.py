from __future__ import annotations

from typing import Sequence

import httpx

from app.ai.config import LLMRuntimeConfig
from app.ai.providers.base import BaseChatModel, ChatMessage, LLMResult


class OllamaChat(BaseChatModel):
    def __init__(self, config: LLMRuntimeConfig) -> None:
        super().__init__(config)
        base = config.base_url or "http://localhost:11434"
        self.base_url = base.rstrip("/")
        self.client = httpx.AsyncClient(timeout=config.request_timeout)

    async def generate(self, messages: Sequence[ChatMessage], **kwargs) -> LLMResult:
        payload: dict = {
            "model": self.config.model,
            "messages": [m.__dict__ for m in messages],
            "stream": False,
        }
        if self.config.max_output_tokens:
            payload["options"] = {"num_predict": self.config.max_output_tokens}

        response = await self.client.post(f"{self.base_url}/api/chat", json=payload)
        response.raise_for_status()
        data = response.json()
        message = data.get("message") or {}
        content = message.get("content") or ""
        return LLMResult(content=content, model=self.config.model, provider="ollama", raw=data)

    async def aclose(self) -> None:
        await self.client.aclose()
