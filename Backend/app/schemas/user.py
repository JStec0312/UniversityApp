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

class VerificationInfoIn(BaseModel):
    role: RoleEnum = RoleEnum.STUDENT
    faculty_id: Optional[int] = None
    major_id: Optional[int] = None
    group_id: Optional[int] = None

    @model_validator(mode="after")
    def validate_group_requirement(self):
        if self.role != RoleEnum.STUDENT and self.group_id is None:
            raise ValueError("group_id is required when role is not student")
        return self