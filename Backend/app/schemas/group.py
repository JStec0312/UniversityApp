from pydantic import BaseModel

class GroupCreateIn(BaseModel):
    group_name: str

class GroupCreateOut(BaseModel):
    id: int
    group_name: str
    university_id: int

class GroupByUniOut(BaseModel):
    id: int
    group_name: str
    university_id: int
    class Config:
        orm_mode = True

