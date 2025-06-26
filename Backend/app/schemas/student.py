from pydantic import BaseModel, field_validator, model_validator, EmailStr
from app.utils.role_enum import RoleEnum
from typing import Optional


class StudentVerificationIn(BaseModel):
    faculty_id: Optional[int] = None
    major_id: Optional[int] = None
from pydantic import BaseModel
from typing import Optional


