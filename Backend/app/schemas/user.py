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
    display_name: str
    avatar_image_url: Optional[str] = None  #
    class Config:
        orm_mode = True



class UserAuthIn(BaseModel):
    email: EmailStr
    password: str

class EmailOut(BaseModel):
    email: EmailStr

