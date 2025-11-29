from fastapi import APIRouter

from .endpoints import auth, devices, events, medication_plans, summary, voice, doctor, ai_chat

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(devices.router, prefix="/devices", tags=["devices"])
api_router.include_router(events.router, prefix="/devices/{device_id}/events", tags=["events"])
api_router.include_router(voice.router, prefix="/devices/{device_id}/voice", tags=["voice"])
api_router.include_router(medication_plans.router, prefix="/medication_plans", tags=["medication"])
api_router.include_router(summary.router, prefix="/summary", tags=["summary"])
api_router.include_router(doctor.router, prefix="/doctor", tags=["doctor"])
api_router.include_router(ai_chat.router, prefix="/ai", tags=["ai"])
