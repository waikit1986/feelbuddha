from pydantic import BaseModel


class AiRequest(BaseModel):
  card: str
  input_text: str

class AiResponse(BaseModel):
  emotion: str
  answer: str
  class Config():
    from_attributes = True