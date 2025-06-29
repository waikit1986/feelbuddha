from uuid import UUID
from pydantic import BaseModel, EmailStr


# class UserBase(BaseModel):
#   username: str
#   email: str
#   password: str

# class UserDisplay(BaseModel):
#   username: str
#   email: str
#   class Config():
#     from_attributes = True
    
# class UsernameDisplay(BaseModel):
#   username: str
#   class Config():
#     from_attributes = True
    
class UserBase(BaseModel):
    user_id: str

class UserResponse(BaseModel):
    user_id: UUID
    email: EmailStr
    is_verified: bool

