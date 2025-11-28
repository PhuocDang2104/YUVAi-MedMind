from pydantic import BaseModel


class VoiceJobOut(BaseModel):
    job_id: str
    device_id: str
    filename: str
