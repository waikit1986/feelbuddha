from sqlalchemy.orm.session import Session
from fastapi import HTTPException, status

from user.schema_user import UserBase
from .schema_wall import WallResponse
from .models_wall import Wall


def get_all_walls(db: Session):
    walls = db.query(Wall).all()

    if not walls:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No post in walls found."
        )

    return [WallResponse.model_validate(wall) for wall in walls]

def post_wall(
    db: Session,
    current_user: UserBase,
    input_text: str
):
    
    wall = Wall(
        user_id=current_user.id,
        username=current_user.username,
        input_text=input_text
    )

    db.add(wall)
    db.commit()
    db.refresh(wall)

    return WallResponse.model_validate(wall)

def delete_wall(
    db: Session,
    wall_id: int,
    current_user: UserBase
):
    wall = db.query(Wall).filter(Wall.id == wall_id).first()

    if not wall:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wall not found"
        )

    if wall.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this wall"
        )

    db.delete(wall)
    db.commit()

    return 'ok'