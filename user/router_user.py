from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from .schema_user import UserBase, UserDisplay
from . import functions_user
from auth.oauth2 import get_current_user


router = APIRouter(
    prefix='/user',
    tags=['User'],
)

@router.post('', response_model=UserDisplay)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    return functions_user.create_user(db, request)

@router.put('', response_model=str)
def update_user(request_user: UserBase, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return functions_user.update_user(request_user, db, current_user)

@router.delete('', response_model=str)
def delete_user(db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return functions_user.delete_user(db, current_user.username) 

