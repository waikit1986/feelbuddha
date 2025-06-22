from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from user.schema_user import UserBase
from .schema_report import ReportBase
from . import functions_report
from auth.oauth2 import get_current_user


router = APIRouter(
    prefix='/report',
    tags=['Report'],
)

@router.post('', response_model=str)
def create_report(request: ReportBase, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return functions_report.create_report(db, request, current_user)

