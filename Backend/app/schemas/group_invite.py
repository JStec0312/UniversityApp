from pydantic import BaseModel

class GroupInviteCreate(BaseModel):
    invited_user_id: int
    group_id: int
    class Config:
        orm_mode = True
    

class GroupInviteOut(BaseModel):
    id: int
    invited_user_id: int
    group_id: int
    status: str

    class Config:
        orm_mode = True