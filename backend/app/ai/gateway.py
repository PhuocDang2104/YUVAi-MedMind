from __future__ import annotations

import json
from typing import Any, Iterable, Sequence

from app.ai.config import LLMRuntimeConfig
from app.ai.prompts import system_prompt_for_mode
from app.ai.providers.base import BaseChatModel, ChatMessage, LLMResult
from app.ai.registry import build_chat_model


class AIGateway:
    """Thin orchestrator that standardizes how the backend talks to LLMs."""

    def __init__(self, config: LLMRuntimeConfig | None = None, chat_model: BaseChatModel | None = None) -> None:
        self.config = config or LLMRuntimeConfig.from_settings()
        self.chat_model = chat_model or build_chat_model(self.config)

    async def run_inference(
        self,
        *,
        mode: str,
        user_message: str,
        context_docs: Iterable[Any] | None = None,
        tool_results: Any | None = None,
        meta: dict[str, Any] | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
        timeout: float | None = None,
        max_tokens: int | None = None,
    ) -> LLMResult:
        messages = self._build_messages(
            mode=mode,
            user_message=user_message,
            context_docs=context_docs or [],
            tool_results=tool_results,
            meta=meta,
        )
        return await self.chat_model.generate(
            messages,
            temperature=temperature,
            top_p=top_p,
            timeout=timeout,
            max_tokens=max_tokens,
        )

    async def aclose(self) -> None:
        await self.chat_model.aclose()

    def _build_messages(
        self,
        *,
        mode: str,
        user_message: str,
        context_docs: Iterable[Any],
        tool_results: Any | None,
        meta: dict[str, Any] | None,
    ) -> Sequence[ChatMessage]:
        system_prompt = system_prompt_for_mode(mode)
        messages: list[ChatMessage] = []
        if system_prompt:
            messages.append(ChatMessage(role="system", content=system_prompt))

        parts: list[str] = [user_message.strip()]
        # Enforce English outputs for consistency across personas.
        parts.append("Respond in English only.")
        if context_docs:
            parts.append(self._format_context(context_docs))
        if tool_results is not None:
            parts.append(self._format_tools(tool_results))
        if meta:
            parts.append(self._format_meta(meta))

        messages.append(ChatMessage(role="user", content="\n\n".join(p for p in parts if p)))
        return messages

    def _format_context(self, docs: Iterable[Any]) -> str:
        formatted: list[str] = []
        for idx, doc in enumerate(docs, start=1):
            if isinstance(doc, str):
                formatted.append(f"[doc{idx}] {doc}")
            elif isinstance(doc, dict):
                title = doc.get("title") or doc.get("id") or f"doc{idx}"
                body = doc.get("content") or doc.get("text") or json.dumps(doc, ensure_ascii=False)
                formatted.append(f"[{title}] {body}")
            else:
                formatted.append(f"[doc{idx}] {doc}")
        return "Context:\n" + "\n".join(formatted)

    def _format_tools(self, payload: Any) -> str:
        serialized = json.dumps(payload, ensure_ascii=False, indent=2)
        return "Tool results:\n" + serialized

    def _format_meta(self, meta: dict[str, Any]) -> str:
        lines = [f"- {key}: {value}" for key, value in meta.items()]
        return "Request meta:\n" + "\n".join(lines)
