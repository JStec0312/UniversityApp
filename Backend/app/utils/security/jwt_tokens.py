# security/jwt_tokens.py
from datetime import datetime, timedelta, timezone
from uuid import uuid4
from jose import jwt
import os
SECRET = os.getenv("JWT_SECRET", "dev-secret")
ALG = "HS256"

def create_access_token(*, user_id:int, university_id:int, roles:list[str], ttl_sec:int=3600)->str:
    now = datetime.now(timezone.utc)
    my_token = jwt.encode({
        "typ":"access","sub":str(user_id),"university_id":university_id,
        "roles":roles,"iat":int(now.timestamp()),
        "exp":int((now+timedelta(seconds=ttl_sec)).timestamp()),
    }, SECRET, algorithm=ALG)
    return my_token

def create_verify_token(user_id: int, ttl_min: int = 60) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "typ": "verify",
        "sub": str(user_id),
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=ttl_min)).timestamp()),
        "jti": str(uuid4()),
    }
    return jwt.encode(payload, SECRET, algorithm=ALG)