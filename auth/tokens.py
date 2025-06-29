from datetime import timedelta
from datetime import datetime, timezone
from jose import jwt as app_jwt
import os
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=12)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return app_jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
