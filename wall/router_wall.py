from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from user.schema_user import UserBase
from . import functions_wall
from user.functions_user import get_current_user
from wall.schema_wall import WallBase, WallDelete, WallResponse


router = APIRouter(
    prefix='/wall',
    tags=['Wall'],
)

@router.get('', response_model=List[WallResponse])
def get_all_wall(
    db: Session = Depends(get_db),
):
    return functions_wall.get_all_walls(db=db)

@router.post('', response_model=WallResponse)
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

@router.delete('', response_model=str)
def delete_wall(
    payload: WallDelete,
    db: Session = Depends(get_db),
    current_user: UserBase = Depends(get_current_user)
):
    return functions_wall.delete_wall(
        db=db,
        wall_id=payload.id,
        current_user=current_user
    )