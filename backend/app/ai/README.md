# AI Workspace (`backend/app/ai`)

Enterprise-ready landing zone to work with LLMs while keeping the FastAPI backend clean. This folder is the entrypoint for:
- Layer 1 (Gateway/Router): standardize prompts and metadata before hitting a model.
- Layer 2 (Real-time): chat/retrieval/tool-calling flows via `AIGateway`.
- Layer 3 (Analytics/Batched): reuse the same providers for offline jobs.

## Layout
- `config.py` – runtime settings mapped from `.env` (`AI_PROVIDER`, `AI_MODEL`, `AI_BASE_URL`, `AI_API_KEY`, `AI_REQUEST_TIMEOUT_SECONDS`, `AI_MAX_OUTPUT_TOKENS`).
- `prompts.py` – system prompts per mode: `patient_chat`, `doctor_chat`, `symptom_extract`, `data_answer`, **layer1_summary**, **layer2_suggestion**.
- `gateway.py` – orchestrator that builds messages with context/tool outputs and calls a provider.
- `patient_layers.py` – merged AI demo logic (layer 1 summary + layer 2 advice) wired to Postgres data for patient flows.
- `patient_responder.py` – patient-facing intent+reply (LOG_SYMPTOM / ASK_MEDICATION / SMALL_TALK) for auto-replies on the device chat.
- `data/` – sample JSON copied from the original `ai_demo` (kept for reference).
- `providers/` – pluggable clients (`openai_chat.py` for OpenAI/vLLM/TGI compatible endpoints, `ollama_chat.py` for on-prem inference).
- `registry.py` – factory to choose a provider from config.
- `__init__.py` – convenience exports.
- `app/services/llm_pipeline.py` – backend-facing shim that calls `AIGateway` (use from REST endpoints or workers).

## Configure
Set the provider/model in `.env` (or `.env.example`):
```
AI_PROVIDER=openai           # openai | openai-compatible | vllm | tgi | ollama
AI_MODEL=openai/gpt-4o-mini   # use openai/gpt-4o-mini for OpenRouter
# AI_BASE_URL=http://localhost:8000/v1      # for vLLM/TGI/openai-compatible
# AI_API_KEY=...                            # required for OpenAI/Azure (aliases: OPENAI_API_KEY, openai_api_key)
# OPENAI_BASE_URL=https://openrouter.ai/api/v1  # accepted alias for AI_BASE_URL
AI_REQUEST_TIMEOUT_SECONDS=30
# Optional OpenRouter headers (strongly recommended)
AI_CLIENT_REFERER=http://localhost:3000
AI_CLIENT_TITLE=MedMind Portal
# AI_MAX_OUTPUT_TOKENS=512
```

## Patient daily summary → suggestion (merged AI demo)
- **Layer 1** (`layer1_summary`): reads latest symptom logs (24–48h) for default patient **Asha Pillai** (or `patient_id` override), current meds (active medication plan), and profile notes. Returns JSON: `physical_summary[]`, `mental_note`, `warning_flag`, `narrative`.
- **Layer 2** (`layer2_suggestion`): consumes layer-1 report + meds + adherence (last 7d dose occurrences) to produce 1 paragraph of advice in Vietnamese, with escalation if `warning_flag` or severe symptoms.
- **REST endpoint**: `POST /api/ai/chat`
  - Body: `{"question": "Tóm tắt tình hình bệnh nhân", "mode": "summary", "patient_id": "..."?}`
  - Body: `{"question": "Có suggestion gì không?", "mode": "suggestion", "patient_id": "..."?}`
  - Response:
    ```json
    {
      "patient_id": "...",
      "patient_name": "Asha Pillai",
      "mode": "summary",
      "layer": 1,
      "message": "<narrative>",
      "warning_flag": true,
      "report": {
        "physical_summary": [{"time": "2025-11-29 07:00", "symptom": "Chest pain", "severity": "severe"}],
        "mental_note": "Lo lắng",
        "warning_flag": true
      }
    }
    ```
- **Data sources**: `symptom_logs`, `medication_plans` + `medication_plan_items` (+ `medications`), `dose_occurrences`, `patient_profiles`, `patients.notes`. Side effects are hinted via a small default mapping (`Amlodipine`, `Atorvastatin`, `Nitroglycerin`, `Beta blocker`).
- **Failover**: If the LLM provider rejects/401/timeout, the backend returns a deterministic fallback summary/suggestion so the UI still responds (narrative notes the fallback).

## Patient auto-reply (Edge device chat)
- Mode: `patient_edge` (see `prompts.py`).
- Intent classifier + reply: `patient_responder.py` → used by `/doctor/symptom_analytics/messages` when direction=IN. It classifies intent into `LOG_SYMPTOM | ASK_MEDICATION | SMALL_TALK` and generates a short, patient-friendly reply. Both the incoming and auto-reply messages are stored in `edge_text_logs.intent`.
- Frontend table shows `intent` in Edge Text Storage; when a message is marked as received, the backend auto-reply is created and logged.

## Use in backend code
```python
from app.ai import AIGateway

gateway = AIGateway()  # auto-loads env config

result = await gateway.run_inference(
    mode="patient_chat",
    user_message="Tui quen uong thuoc huyet ap toi qua, phai lam sao?",
    context_docs=[{"title": "med_guideline", "content": "Never double the dose; skip and continue schedule."}],
    tool_results={"adherence": {"last_7d": 0.78}},
    meta={"patient_id": "demo-patient", "channel": "device"},
)
print(result.content)
```

To wire voice → ASR → LLM, use `LLMPipeline`:
```python
from app.services.llm_pipeline import LLMPipeline

pipeline = LLMPipeline()
voice_meta = pipeline.process_voice(device_id, "/path/to/audio.wav")
# After ASR produces text:
# await pipeline.run_text(mode="symptom_extract", text=asr_text, meta=voice_meta)
```

## Extend providers
1. Add a new client in `providers/` (follow the `BaseChatModel` interface).
2. Register it in `registry.py`.
3. Expose provider-specific env vars in `config.py`/`.env.example`.

This keeps model swaps (OpenAI ↔ vLLM ↔ Ollama) contained without touching the rest of the backend. The frontend chat widget (floating button) calls `/api/ai/chat` for the two-layer flow above; keep that endpoint stable for UI interoperability.
