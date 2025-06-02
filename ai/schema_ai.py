from pydantic import BaseModel


class AiRequest(BaseModel):
  card: str
  situation: str

class AiResponse(BaseModel):
  emotion: str
  answer: str
  class Config():
    from_attributes = True