from datetime import datetime
from pydantic import BaseModel
from uuid import UUID


class ReadingResponse(BaseModel):
    id: UUID
    created_at: datetime
    card: str
    input_text: str
    emotion: str
    answer: str

    class Config:
        from_attributes = True