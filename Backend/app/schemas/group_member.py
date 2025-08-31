from pydantic import BaseModel

class GroupMemberOut(BaseModel):
    id: int
    user_id: int
    group_id: int
    created_at: str

    class Config:
        orm_mode = True