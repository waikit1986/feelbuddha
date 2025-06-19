from pydantic import BaseModel
from uuid import UUID


class ReportBase(BaseModel):
    reported_wall: UUID
    reporting_user_id: UUID