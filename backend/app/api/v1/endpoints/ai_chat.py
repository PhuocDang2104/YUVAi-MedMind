from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.ai.patient_layers import generate_layer1_summary, generate_layer2_suggestion
from app.db.session import get_db
from app.schemas.ai_chat import ChatRequest, ChatResponse, Layer1Report

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def ai_chat(payload: ChatRequest, db: Session = Depends(get_db)) -> ChatResponse:
    mode = payload.mode.lower()
    if mode == "summary":
        result = await generate_layer1_summary(db, patient_id=payload.patient_id)
        report = result.get("report")
        return ChatResponse(
            patient_id=result["patient_id"],
            patient_name=result["patient_name"],
            mode="summary",
            layer=1,
            message=result["narrative"],
            narrative=result["narrative"],
            warning_flag=result.get("warning_flag"),
            report=Layer1Report(**report) if isinstance(report, dict) else None,
        )

    if mode == "suggestion":
        result = await generate_layer2_suggestion(db, patient_id=payload.patient_id)
        report = result.get("report")
        return ChatResponse(
            patient_id=result["patient_id"],
            patient_name=result["patient_name"],
            mode="suggestion",
            layer=2,
            message=result["message"],
            narrative=result.get("narrative"),
            warning_flag=result.get("warning_flag"),
            report=Layer1Report(**report) if isinstance(report, dict) else None,
        )

    raise HTTPException(status_code=400, detail="Unsupported mode")
