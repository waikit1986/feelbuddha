from pydantic import BaseModel
from uuid import UUID


class ReadingResponse(BaseModel):
    id: UUID
    card: str
    situation: str
    emotion: str
    answer: str

    class Config:
        from_attributes = True