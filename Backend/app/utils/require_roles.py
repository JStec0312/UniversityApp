from fastapi import Request, Depends, HTTPException
from jose import jwt, JWTError
from app.utils.role_enum import RoleEnum
import os

SECRET_KEY = os.getenv("JWT_SECRET")

def require_roles(allowed_roles: list[str]):
    def _require(request: Request):
        token = request.cookies.get("access_token")  
        if not token:
            raise HTTPException(
                status_code=401,
                detail="Missing authentication token"
            )

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            role: str = payload.get("role")
            if role not in allowed_roles:
                raise HTTPException(
                    status_code=403,
                    detail="Operation not permitted for this role"
                )
            return {"user_id": int(payload.get("sub")), "role": role}
        except JWTError:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials"
            )
    return _require
