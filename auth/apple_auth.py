import os
import time
import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from jose import jwt, jwk, JWTError
from jose.utils import base64url_decode
import httpx
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Auth"])

APPLE_KEYS_URL = "https://appleid.apple.com/auth/keys"
APPLE_TOKEN_URL = "https://appleid.apple.com/auth/token"

class AppleAuthRequest(BaseModel):
    code: str
    id_token: str

def generate_apple_client_secret():
    try:
        headers = {
            "kid": os.getenv("APPLE_KEY_ID"),
            "alg": "ES256"
        }

        with open(os.getenv("APPLE_PRIVATE_KEY_PATH")) as f:
            private_key = f.read()

        claims = {
            "iss": os.getenv("APPLE_TEAM_ID"),
            "iat": int(time.time()),
            "exp": int(time.time()) + 86400 * 180,
            "aud": "https://appleid.apple.com",
            "sub": os.getenv("APPLE_CLIENT_ID")
        }

        return jwt.encode(
            payload=claims,
            key=private_key,
            algorithm="ES256",
            headers=headers
        )
    except Exception as e:
        logger.error(f"Failed to generate client secret: {e}")
        raise HTTPException(status_code=500, detail="Internal server error generating Apple client secret")

async def exchange_code_for_token(code: str):
    data = {
        "client_id": os.getenv("APPLE_CLIENT_ID"),
        "client_secret": generate_apple_client_secret(),
        "code": code,
        "grant_type": "authorization_code",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(APPLE_TOKEN_URL, data=data)
        if response.status_code != 200:
            logger.error(f"Apple token exchange failed: {response.text}")
            raise HTTPException(status_code=400, detail=f"Apple token exchange error: {response.text}")
        return response.json()

async def verify_identity_token(id_token: str):
    try:
        async with httpx.AsyncClient() as client:
            keys = (await client.get(APPLE_KEYS_URL)).json()["keys"]

        headers = jwt.get_unverified_header(id_token)
        key = next((k for k in keys if k["kid"] == headers["kid"]), None)
        if not key:
            logger.error("Apple public key not found")
            raise HTTPException(status_code=400, detail="Apple public key not found")

        public_key = jwk.construct(key)
        message, encoded_signature = id_token.rsplit('.', 1)
        decoded_signature = base64url_decode(encoded_signature.encode())

        if not public_key.verify(message.encode(), decoded_signature):
            logger.error("Invalid Apple identity token signature")
            raise HTTPException(status_code=400, detail="Invalid Apple identity token signature")

        claims = jwt.decode(
            id_token,
            key=public_key.to_pem(),
            algorithms=["RS256"],
            audience=os.getenv("APPLE_CLIENT_ID")
        )

        return claims

    except JWTError as e:
        logger.error(f"JWT decode failed: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid identity token: {str(e)}")
    except Exception as e:
        logger.error(f"verify_identity_token failed: {e}")
        raise HTTPException(status_code=400, detail=f"Apple identity token verification error: {str(e)}")

@router.post("/auth/apple")
async def apple_auth(payload: AppleAuthRequest):
    try:
        claims = await verify_identity_token(payload.id_token)
    except HTTPException as ve:
        # Already handled
        raise ve
    except Exception as e:
        logger.exception("Unhandled error during token verification")
        raise HTTPException(status_code=400, detail="Unhandled error during identity token verification")

    try:
        token_data = await exchange_code_for_token(payload.code)
    except HTTPException as ve:
        # Already handled
        raise ve
    except Exception as e:
        logger.exception("Unhandled error during token exchange")
        raise HTTPException(status_code=400, detail="Unhandled error during token exchange")

    try:
        user_id = claims["sub"]
        email = claims.get("email")
        email_verified = claims.get("email_verified")

        return {
            "status": "success",
            "user": {
                "apple_id": user_id,
                "email": email,
                "email_verified": email_verified
            },
            "tokens": token_data
        }

    except Exception as e:
        logger.exception("Failed to construct response")
        raise HTTPException(status_code=500, detail="Internal server error preparing user data")
