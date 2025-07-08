from pydantic import BaseModel
from datetime import datetime

class GroupRegisterPasswordCreate(BaseModel):
    group_id: int
    expires_at: datetime  # ISO 8601 format, e.g., "2023-12-31T23:59:59"

class GroupRegisterPasswordOut(BaseModel):
    token: str
    group_id:int
    expires_at: datetime