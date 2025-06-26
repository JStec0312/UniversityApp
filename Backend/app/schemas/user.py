from pydantic import BaseModel, field_validator, model_validator, EmailStr
from app.utils.role_enum import RoleEnum
from typing import Optional
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    display_name: str 
    university_id: int

class UserOut(BaseModel):
    id: int
    email: EmailStr
    display_name: str

    class Config:
        orm_mode = True
