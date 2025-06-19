from sqlalchemy.orm.session import Session
from fastapi import HTTPException, status

from user.schema_user import UserBase
from .models_report import  Report
from .schema_report import ReportBase


def create_report(db: Session, request: ReportBase):
  new_report = Report(
      wall_id=request.reported_wall,
      reporting_user_id=request.reporting_user_id
  )
  db.add(new_report)
  db.commit()
  db.refresh(new_report)
  return 'ok'


