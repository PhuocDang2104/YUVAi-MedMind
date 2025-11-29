from typing import Literal, Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(..., description="User question in vi/en")
    mode: Literal["summary", "suggestion"] = Field(
        ..., description="summary = layer 1, suggestion = layer 2 building on layer 1"
    )
    patient_id: Optional[str] = Field(None, description="Defaults to demo patient Asha Pillai when omitted")


class PhysicalSummary(BaseModel):
    time: str
    symptom: str
    severity: Optional[str] = None


class Layer1Report(BaseModel):
    physical_summary: list[PhysicalSummary] = Field(default_factory=list)
    mental_note: Optional[str] = None
    warning_flag: Optional[bool] = None


class ChatResponse(BaseModel):
    patient_id: str
    patient_name: str
    mode: Literal["summary", "suggestion"]
    layer: int
    message: str
    report: Optional[Layer1Report] = None
    warning_flag: Optional[bool] = None
    narrative: Optional[str] = None
