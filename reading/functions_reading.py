from sqlalchemy.orm.session import Session
from fastapi import HTTPException, status

from user.schema_user import UserBase
from .schema_reading import ReadingResponse
from .models_reading import Reading


def get_all_readings(current_user: UserBase, db: Session):
    readings = db.query(Reading).filter(Reading.user_id == current_user.id).all()

    if not readings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No readings found for this user."
        )

    return [ReadingResponse.model_validate(reading) for reading in readings]


