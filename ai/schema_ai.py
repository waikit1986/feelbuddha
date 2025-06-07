from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class AiRequest(BaseModel):
  card: str
  situation: str

class AiResponse(BaseModel):
  id: UUID
  created_at: datetime
  card: str
  situation: str
  emotion: str
  answer: str
  class Config():
    from_attributes = True