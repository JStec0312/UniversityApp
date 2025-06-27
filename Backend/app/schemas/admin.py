from pydantic import BaseModel, field_validator, model_validator, EmailStr
from app.utils.role_enum import RoleEnum
from typing import Optional


class AdminVerificationIn(BaseModel):
    group_id: int

class AdminAuthIn(BaseModel):
    email: EmailStr
    password: str

class AdminAuthOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: RoleEnum = RoleEnum.ADMIN
    admin_id: int
    university_id: int
    user_id: int
    email: EmailStr
    display_name: str
    group_id: int
    
