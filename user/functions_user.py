from uuid import UUID
from sqlalchemy import func
from sqlalchemy.orm.session import Session
from fastapi import HTTPException, status

from db.hash import Hash
from .schema_user import UserBase
from .models_user import User


def create_user(db: Session, request: UserBase):
  if db.query(User).filter(User.username == request.username).first():
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
        detail="Username already used, please create a new one."
    )
    
  if db.query(User).filter(User.email == request.email).first():
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Email already exists. Please login instead."
    )

  new_user = User(
    username=request.username,
    email=request.email,
    password=Hash.bcrypt(request.password)
  )
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user

def get_user_by_username(db: Session, username: str):
  user = db.query(User).filter(User.username == username).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
      detail=f'User with username {username} not found')
  return user

def update_user(db: Session, username: str, request: UserBase):
  user = db.query(User).filter(User.username == username).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
      detail=f'User with username {username} not found')
  user.username = request.username
  user.email = request.email
  user.password = Hash.bcrypt(request.password)
  db.commit()
  return 'ok'

def delete_user(db: Session, username: str):
  user = db.query(User).filter(User.username == username).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
      detail='User with username {username} not found')
  db.delete(user)
  db.commit()
  return 'ok'