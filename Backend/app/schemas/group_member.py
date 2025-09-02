from pydantic import BaseModel, ConfigDict

class GroupMemberOut(BaseModel):
    id: int
    user_id: int
    group_id: int

    class Config:
        orm_mode = True

class GroupMemberOutDisplayName(BaseModel):
    id: int
    user_id: int
    group_id: int
    display_name: str
    model_config = ConfigDict(
        orm_mode=True,
        from_attributes=True
    )

class GroupAdminCreate(BaseModel):
    invited_user_id: int
    