"""
Placeholder service to orchestrate ASR + LLM pipeline.
"""

from typing import Any


class LLMPipeline:
    def __init__(self) -> None:
        self.name = "llm-pipeline"

    def process_voice(self, device_id: str, audio_path: str) -> dict[str, Any]:
        # TODO: integrate ASR, intent classification, extraction, notification hooks
        return {"device_id": device_id, "audio_path": audio_path, "intent": "LOG_SYMPTOM"}
