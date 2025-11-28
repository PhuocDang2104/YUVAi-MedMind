from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.voice import VoiceJobOut

router = APIRouter()


@router.post("")
async def upload_voice(device_id: str, file: UploadFile, db: Session = Depends(get_db)) -> VoiceJobOut:
    # TODO: store audio, enqueue ASR/LLM pipeline, return job id
    return VoiceJobOut(job_id="voice-job-demo", device_id=device_id, filename=file.filename or "audio.wav")
