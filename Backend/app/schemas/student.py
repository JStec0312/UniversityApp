from pydantic import BaseModel, field_validator, model_validator, EmailStr
from app.utils.role_enum import RoleEnum
from typing import Optional


class StudentVerificationIn(BaseModel):
    faculty_id: Optional[int] = None
    major_id: Optional[int] = None
from pydantic import BaseModel
from typing import Optional


class StudentAuthIn(BaseModel):
    email: EmailStr
    password: str

class StudentAuthOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: RoleEnum = RoleEnum.STUDENT
    student_id: int
    university_id: int
    user_id: int
    student_id: int
    email: EmailStr
    display_name: str
    faculty_id: Optional[int] = None
    major_id: Optional[int] = None