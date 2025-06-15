from datetime import datetime
from pydantic import BaseModel
from uuid import UUID


class WallBase(BaseModel):
    input_text: str

    class Config:
        from_attributes = True
        
class WallDisplay(BaseModel):
    id: UUID
    created_at: datetime
    username: str
    input_text: str

    class Config:
        from_attributes = True