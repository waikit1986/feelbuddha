from datetime import datetime
from pydantic import BaseModel
from uuid import UUID


class ReadingResponse(BaseModel):
    id: UUID
    created_at: datetime
    sutra_name: str
    sutra_excerpt: str
    saint: str
    advice: str
    practice: str

    class Config:
        from_attributes = True