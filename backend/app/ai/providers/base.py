from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

from app.ai.config import LLMRuntimeConfig


@dataclass
class ChatMessage:
    role: str
    content: str


@dataclass
class LLMResult:
    content: str
    model: str
    provider: str
    raw: Any


class BaseChatModel:
    def __init__(self, config: LLMRuntimeConfig) -> None:
        self.config = config

    async def generate(self, messages: Sequence[ChatMessage], **kwargs: Any) -> LLMResult:
        raise NotImplementedError

    async def aclose(self) -> None:
        return None
