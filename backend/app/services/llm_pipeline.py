"""Enterprise-friendly LLM entrypoint that the backend can plug into."""

from __future__ import annotations

from typing import Any, Iterable

from app.ai.gateway import AIGateway


class LLMPipeline:
    def __init__(self, gateway: AIGateway | None = None) -> None:
        self.gateway = gateway or AIGateway()

    async def run_text(
        self,
        *,
        mode: str,
        text: str,
        context_docs: Iterable[Any] | None = None,
        tool_results: Any | None = None,
        meta: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Generic hook used by REST endpoints or workers to hit the AI Gateway.
        """
        result = await self.gateway.run_inference(
            mode=mode,
            user_message=text,
            context_docs=context_docs,
            tool_results=tool_results,
            meta=meta,
        )
        return {"content": result.content, "model": result.model, "provider": result.provider}

    def process_voice(self, device_id: str, audio_path: str) -> dict[str, Any]:
        """
        Called after audio is stored. ASR should push the transcript into run_text().
        """
        return {
            "device_id": device_id,
            "audio_path": audio_path,
            "intent": "LOG_SYMPTOM",
            "entrypoint": "app.ai.AIGateway",
        }
