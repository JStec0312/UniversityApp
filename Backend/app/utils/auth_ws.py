# app/utils/ws_auth.py
from jose import jwt, JWTError
from fastapi import WebSocket
import os

SECRET_KEY = os.getenv("JWT_SECRET")  # upewnij się, że ustawione

async def auth_ws(websocket: WebSocket, allowed_roles: list[str]):
    token = websocket.cookies.get("access_token")

    if not token:
        await websocket.close(code=1008, reason="Missing authentication token")
        return None

    if not SECRET_KEY:
        await websocket.close(code=1011, reason="Server misconfig (no SECRET)")
        return None

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        role = payload.get("role")
        if role not in allowed_roles:
            await websocket.close(code=1008, reason="Operation not permitted for this role")
            return None
        return {
            "user_id": int(payload.get("sub")),
            "role": role,
            "university_id": payload.get("university_id"),
        }
    except JWTError:
        await websocket.close(code=1008, reason="Invalid authentication credentials")
        return None
