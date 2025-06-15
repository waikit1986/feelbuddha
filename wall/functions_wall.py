from sqlalchemy.orm.session import Session
from fastapi import HTTPException, status

from user.functions_user import get_user_by_username
from user.schema_user import UserBase
from .schema_wall import WallDisplay
from .models_wall import Wall


def get_all_walls(db: Session):
    walls = db.query(Wall).all()

    if not walls:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No post in walls found."
        )

    return [WallDisplay.model_validate(wall) for wall in walls]

def post_wall(
    db: Session,
    current_user: UserBase,
    input_text: str
):
    user = get_user_by_username(db, current_user.username)
    
    wall = Wall(
        user_id=user.id,
        username=user.username,
        input_text=input_text
    )

    db.add(wall)
    db.commit()
    db.refresh(wall)

    return WallDisplay.model_validate(wall)