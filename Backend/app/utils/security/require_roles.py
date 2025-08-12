from typing import Sequence
from fastapi import Request, Depends, HTTPException
from jose import jwt, JWTError, ExpiredSignatureError
import os

SECRET_KEY = os.getenv("JWT_SECRET", "dev-secret")
ALG = "HS256"

def _parse_user_from_cookie(request: Request) -> dict:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(401, "Missing authentication token")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALG])  # sprawdza też exp
    except ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except JWTError:
        raise HTTPException(401, "Invalid authentication credentials")

    try:
        user_id = int(payload["sub"])
        university_id = int(payload["university_id"])
    except (KeyError, ValueError, TypeError):
        raise HTTPException(401, "Invalid authentication payload")

    roles = payload.get("roles", [])
    if not isinstance(roles, list):
        roles = [str(roles)]

    return {"user_id": user_id, "university_id": university_id, "roles": roles, "raw": payload}

def require_roles(allowed_roles: Sequence[str]):
    def _require(user = Depends(_parse_user_from_cookie)):
        if not set(allowed_roles) & set(user["roles"]):
            raise HTTPException(403, "Operation not permitted for this role")
        return user
    return _require
