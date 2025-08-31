from pydantic import BaseModel, field_validator, model_validator, EmailStr
from app.utils.enums.role_enum import RoleEnum
from typing import Optional


class StudentVerificationIn(BaseModel):
    token: str
    faculty_id: Optional[int] = None
    major_id: Optional[int] = None
from pydantic import BaseModel
from typing import Optional


class StudentOut(BaseModel):
    student_id: int
    university_id: int
    user_id: int
    display_name: str
    faculty_id: Optional[int] = None
    major_id: Optional[int] = None
    avatar_image_url: Optional[str] = None  # URL to the student's avatar image

class StudentAuthIn(BaseModel):
    email: EmailStr
    password: str

class StudentAuthOut(BaseModel):
    student: StudentOut


class StudentMeOut(BaseModel):
    role: RoleEnum = RoleEnum.STUDENT
    user_id: int
    email: EmailStr
    display_name: str
    faculty_id: Optional[int] = None
    major_id: Optional[int] = None
    university_id: int
