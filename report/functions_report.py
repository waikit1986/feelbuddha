from sqlalchemy.orm.session import Session
from fastapi import HTTPException, status

from user.schema_user import UserBase
from .models_report import  Report
from .schema_report import ReportBase
from user.models_user import User


def create_report(db: Session, request: ReportBase, current_user: UserBase):

  user = db.query(User).filter(User.username == current_user.username).first()
  if not user:
      raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND,
          detail=f'User with username {current_user.username} not found'
      )

  new_report = Report(
      wall_id=request.reported_wall,
      reporting_user_id=user.id
  )
  
  db.add(new_report)
  db.commit()
  db.refresh(new_report)
  return 'ok'


