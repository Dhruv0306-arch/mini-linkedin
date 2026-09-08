from datetime import datetime
from pydantic import BaseModel

class ApplicationCreate(BaseModel):
    cover_note: str | None = None

class ApplicationOut(BaseModel):
    id: int
    job_id: int
    user_id: int
    cover_note: str | None
    created_at: datetime

    class Config:
        from_attributes = True

