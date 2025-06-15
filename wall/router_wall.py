from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from user.schema_user import UserBase
from . import functions_wall
from auth.oauth2 import get_current_user
from wall.schema_wall import WallBase, WallDisplay


router = APIRouter(
    prefix='/wall',
    tags=['Wall'],
)

@router.get('', response_model=List[WallDisplay])
def get_all_wall(
    db: Session = Depends(get_db),
):
    return functions_wall.get_all_walls(db=db)

@router.post('', response_model=WallDisplay)
def post_wall(
    payload: WallBase,
    db: Session = Depends(get_db),
    current_user: UserBase = Depends(get_current_user)
):
    return functions_wall.post_wall(
        db=db,
        current_user=current_user,
        input_text=payload.input_text
    )
