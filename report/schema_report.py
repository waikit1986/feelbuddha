from pydantic import BaseModel
from uuid import UUID


class ReportBase(BaseModel):
    reported_wall: UUID