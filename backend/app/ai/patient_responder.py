from __future__ import annotations

import json
import re
from typing import Tuple

from app.ai.gateway import AIGateway

INTENTS = {"LOG_SYMPTOM", "ASK_MEDICATION", "SMALL_TALK"}


def _detect_intent_local(text: str) -> str:
    t = text.lower()
    if any(kw in t for kw in ["chest", "pain", "shortness", "breath", "dizzy", "headache", "hurt", "ache", "mệt", "đau", "khó thở"]):
        return "LOG_SYMPTOM"
    if any(kw in t for kw in ["medicine", "medication", "pill", "dose", "when should i", "take", "thuốc", "uống", "liều"]):
        return "ASK_MEDICATION"
    if any(kw in t for kw in ["hello", "hi", "thanks", "thank", "how are you", "chào", "cảm ơn"]):
        return "SMALL_TALK"
    return "SMALL_TALK"


def _template_reply(intent: str, text: str) -> str:
    if intent == "LOG_SYMPTOM":
        if re.search(r"chest|pain|đau ngực", text, re.IGNORECASE):
            return "I noted your chest discomfort. Please sit down, breathe slowly, and contact your caregiver or doctor right away."
        if re.search(r"breath|khó thở|shortness", text, re.IGNORECASE):
            return "I recorded your shortness of breath. Rest now and let your caregiver or doctor know if it worsens."
        return "Thanks for telling me how you feel. I’ve logged your symptom so your caregiver can follow up."
    if intent == "ASK_MEDICATION":
        return "For medication questions, follow your prescribed schedule and do not change doses. If unsure, ask your caregiver or doctor."
    return "Thanks for sharing. I’m here to help log and remind you. Let your caregiver know if you feel unwell."


def _parse_json_response(text: str) -> tuple[str, str]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.replace("```json", "").replace("```", "").strip()
    try:
        data = json.loads(cleaned)
        intent = str(data.get("intent") or "").strip().upper() or "SMALL_TALK"
        reply = str(data.get("reply") or "").strip()
        return intent, reply or ""
    except Exception:
        return "SMALL_TALK", cleaned or "Thanks for sharing. I’ve noted this."


async def classify_and_reply_patient(
    text: str,
    *,
    gateway: AIGateway | None = None,
) -> tuple[str, str]:
    local_intent = _detect_intent_local(text)
    gw = gateway or AIGateway()
    owns = gateway is None
    intent, reply = local_intent, _template_reply(local_intent, text)
    try:
        result = await gw.run_inference(mode="patient_edge", user_message=text)
        ai_intent, ai_reply = _parse_json_response(result.content)
        if ai_intent not in INTENTS:
            ai_intent = local_intent
        intent = ai_intent
        reply = ai_reply or _template_reply(intent, text)
    except Exception:
        # fallback stays with local intent/template
        pass
    finally:
        if owns:
            await gw.aclose()
    return intent, reply
