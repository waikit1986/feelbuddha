from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime, timezone
from typing import Optional
from jose import jwt, jwk
import httpx
import hashlib
import os
from dotenv import load_dotenv
import json
from sqlalchemy.orm import Session

from db.database import get_db
from user.models_user import User
from . tokens import create_access_token

load_dotenv()

router = APIRouter(
    prefix="/apple",
    tags=["Apple Authentication"]
)

APPLE_CLIENT_ID = os.getenv("APPLE_CLIENT_ID")

class AppleAuthRequest(BaseModel):
    id_token: str
    nonce: str
    user_identifier: str
    email: Optional[str] = None
    full_name: Optional[str] = None

async def get_apple_public_key(kid: str) -> Optional[dict]:
    async with httpx.AsyncClient() as client:
        response = await client.get("https://appleid.apple.com/auth/keys")
        keys = response.json().get("keys", [])
        return next((k for k in keys if k["kid"] == kid), None)

async def verify_apple_token(id_token: str, nonce: str) -> dict:
    try:
        print(f"Verifying Apple ID token, nonce: {nonce}")
        header = jwt.get_unverified_header(id_token)
        kid = header.get("kid")
        print(f"Apple token key ID: {kid}")

        public_key_data = await get_apple_public_key(kid)
        if not public_key_data:
            raise HTTPException(400, detail="Apple public key not found")

        public_key = jwk.construct(public_key_data)

        decoded = jwt.decode(
            id_token,
            key=public_key,
            algorithms=["RS256"],
            audience=APPLE_CLIENT_ID,
            issuer="https://appleid.apple.com",
            options={"verify_nonce": False}
        )

        print(f"Decoded Apple ID token:\n{json.dumps(decoded, indent=2)}")

        expected_nonce_hash = hashlib.sha256(nonce.encode()).hexdigest()
        token_nonce = decoded.get("nonce")
        print(f"Token nonce: {token_nonce}")
        print(f"Expected SHA256 nonce hash: {expected_nonce_hash}")

        if not token_nonce or token_nonce.lower() != expected_nonce_hash.lower():
            raise HTTPException(400, detail=f"Nonce mismatch!\nReceived: {token_nonce}\nExpected: {expected_nonce_hash}")

        return decoded

    except jwt.ExpiredSignatureError:
        raise HTTPException(400, detail="Apple ID token has expired")
    except jwt.JWTError as e:
        raise HTTPException(400, detail=f"Invalid Apple ID token: {e}")
    except Exception as e:
        raise HTTPException(400, detail=f"Apple token verification failed: {e}")

@router.post("/login")
async def auth_apple(request: AppleAuthRequest, db: Session = Depends(get_db)):
    try:
        decoded = await verify_apple_token(request.id_token, request.nonce)
        apple_sub = decoded["sub"]
        now = datetime.now(timezone.utc)

        user = db.query(User).filter(User.apple_sub == apple_sub).first()

        if user:
            print("Found existing user with Apple sub:", apple_sub)
            user.last_login = now

            updated_email = decoded.get("email") or request.email
            if updated_email and updated_email != user.email:
                user.email = updated_email

            verified_flag = decoded.get("email_verified", user.email_verified)
            if verified_flag != user.email_verified:
                user.email_verified = verified_flag

            if not user.full_name and request.full_name:
                user.full_name = request.full_name
                
            access_token = create_access_token(data={"sub": str(user.id)})

            print("Updated user:", user)

        else:
            user = User(
                apple_sub=apple_sub,
                full_name=request.full_name or None,
                email=decoded.get("email", request.email),
                email_verified=decoded.get("email_verified", False),
                created_at=now,
                last_login=now
            )
            print("Creating new user with Apple sub:", apple_sub)
            db.add(user)
            
            access_token = create_access_token(data={"sub": str(user.id)})

        db.commit()
        db.refresh(user)

        return {
            "status": "success",
            "user_id": str(user.id),
            "email": user.email,
            "is_verified": user.email_verified,
            "username": user.username,
            "access_token": access_token
        }

    except HTTPException as e:
        print(f"Apple Auth Error: {e.detail}")
        raise e
