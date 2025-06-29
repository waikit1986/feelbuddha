from datetime import timedelta, datetime, timezone
from jose import jwt as app_jwt
import os
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"

def create_access_token(user, expires_delta: timedelta = timedelta(hours=12)):
    """
    Creates a JWT access token including the Apple user ID (`sub`).
    """
    to_encode = {
        "sub": user.apple_sub,             
        "user_id": str(user.id),           
        "email": user.email,
        "username": user.username,
    }
    
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode["exp"] = expire

    return app_jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
