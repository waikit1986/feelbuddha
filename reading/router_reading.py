from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from user.schema_user import UserBase
from . import functions_reading
from auth.oauth2 import get_current_user
from reading.schema_reading import ReadingResponse


router = APIRouter(
    prefix='/reading',
    tags=['Reading'],
)

@router.get('', response_model=List[ReadingResponse])
def get_my_readings(
    db: Session = Depends(get_db),
    current_user: UserBase = Depends(get_current_user)
):
    return functions_reading.get_all_readings(current_user=current_user, db=db)
