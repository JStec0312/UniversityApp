from pydantic import BaseModel
from datetime import datetime

class GroupCreateIn(BaseModel):
    group_name: str

class GroupCreateOut(BaseModel):
    group_id: int
    group_name: str
    university_id: int
    