from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from db.database import get_db
from user import models_user
from db.hash import Hash
from auth import oauth2


router = APIRouter(
    tags=["Auth"]
)

@router.post('/token')
def get_token(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models_user.User).filter(models_user.User.username == request.username).first()
    if not user: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect credentials")

    user.last_login = datetime.now(timezone.utc)
    db.commit()
    
    access_token = oauth2.create_access_token(data={"sub": user.username})
    
    return {"access_token": access_token, "token_type": "bearer", "user_id": user.id, "username": user.username, "email": user.email}

