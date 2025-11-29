from app.ai.config import LLMRuntimeConfig
from app.ai.providers.base import BaseChatModel
from app.ai.providers.ollama_chat import OllamaChat
from app.ai.providers.openai_chat import OpenAIChat


def build_chat_model(config: LLMRuntimeConfig) -> BaseChatModel:
    provider = (config.provider or "").lower()
    if provider in {"openai", "azure_openai", "openai-compatible", "vllm", "tgi", "lmdeploy"}:
        return OpenAIChat(config)
    if provider == "ollama":
        return OllamaChat(config)
    raise ValueError(f"Unsupported ai_provider: {config.provider}")
