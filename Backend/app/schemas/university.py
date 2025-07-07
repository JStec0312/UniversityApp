from pydantic import BaseModel, field_validator, model_validator, EmailStr
from app.utils.role_enum import RoleEnum
from typing import Optional

class UniversityOut(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True