from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

class ConnectionService:
    def __init__(self):
        self.active: List[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)

    def disconnect(self, ws: WebSocket):
        self.active.remove(ws)

    async def broadcast(self, msg: str):
        for ws in self.active:
            await ws.send_text(msg)

