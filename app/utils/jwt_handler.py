from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import os
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "mysecret")
JWT_ALGORITHM = "HS256"

# Use Bearer Token authentication
security = HTTPBearer()


def create_jwt(payload: dict, expires_minutes: int = 60 * 24):
    to_encode = payload.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode["exp"] = expire

    token = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def decode_jwt(token: str):
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


def get_current_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials  # Extract JWT from Authorization header
    return decode_jwt(token)
