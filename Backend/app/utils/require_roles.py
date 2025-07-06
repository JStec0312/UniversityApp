from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.utils.role_enum import RoleEnum
import os
SECRET_KEY = os.getenv("JWT_SECRET")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "/api/user/student/auth")

def require_roles(allowed_roles: list[str]):
    def _require(token:str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            role: str = payload.get("role")
            if role not in allowed_roles:
                raise HTTPException(
                    status_code=403,
                    detail="Operation not permitted for this role"
                )
            return {"user_id": payload.get("sub"), "role": role}
        except JWTError:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials"
                )
    return _require