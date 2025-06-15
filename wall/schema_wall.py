from datetime import datetime
from pydantic import BaseModel


class WallBase(BaseModel):
    username: str
    input_text: str

    class Config:
        from_attributes = True
        
class WallDisplay(BaseModel):
    created_at: datetime
    username: str
    input_text: str

    class Config:
        from_attributes = True