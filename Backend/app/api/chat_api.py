from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect
from app.utils.auth_ws import auth_ws
from app.utils.role_enum import RoleEnum
import json, time
from typing import Dict, Set

router = APIRouter()

# Store active WebSocket connections
class ConnectionManager:
    def __init__(self):
        # user_id -> set of websockets for that user
        self.active_connections: Dict[int, Set[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()
        self.active_connections[user_id].add(websocket)
    
    def disconnect(self, websocket: WebSocket, user_id: int):
        if user_id in self.active_connections:
            self.active_connections[user_id].discard(websocket)
            if not self.active_connections[user_id]:  # Remove empty sets
                del self.active_connections[user_id]
    
    async def send_personal_message(self, message: dict, user_id: int):
        if user_id in self.active_connections:
            # Send to all connections of this user (multiple tabs/devices)
            disconnected = set()
            for websocket in self.active_connections[user_id]:
                try:
                    await websocket.send_json(message)
                except:
                    disconnected.add(websocket)
            
            # Clean up disconnected websockets
            for ws in disconnected:
                self.active_connections[user_id].discard(ws)
    
    async def send_dm(self, message: dict, from_user: int, to_user: int):
        # Send to both sender and receiver
        await self.send_personal_message(message, from_user)
        await self.send_personal_message(message, to_user)

manager = ConnectionManager()

@router.websocket("/ws/dm")
async def ws_dm(ws: WebSocket, to: int):
    claims = await auth_ws(ws, [RoleEnum.STUDENT.value, RoleEnum.ADMIN.value, RoleEnum.SUPERIOR_ADMIN.value])
    if not claims:  # auth zamknął WS
        return
    me = claims["user_id"]

    await manager.connect(ws, me)
    
    # Send connection confirmation
    await ws.send_json({
        "from": "system",
        "message": f"DM connection established {me}↔{to}",
        "ts": int(time.time() * 1000)
    })

    try:
        while True:
            raw = await ws.receive_text()
            try:
                data = json.loads(raw)
                text = (data.get("message") or "").strip()
            except Exception:
                text = raw.strip()
            
            if not text: 
                continue
            
            # Create message object
            message = {
                "from": me,
                "to": to,
                "message": text,
                "ts": int(time.time() * 1000)
            }
            
            # Send message to both users
            await manager.send_dm(message, me, to)
            
    except WebSocketDisconnect:
        manager.disconnect(ws, me)
