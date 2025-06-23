from datetime import datetime
from pydantic import BaseModel
from uuid import UUID


class ReadingResponse(BaseModel):
    id: UUID
    created_at: datetime
    tradition: str
    input_text: str
    figure_name: str
    figure_story: str
    sutra_name: str
    sutra_excerpt: str
    explanation: str
    advice: str
    practice: str

    class Config:
        from_attributes = True