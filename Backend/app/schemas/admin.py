from pydantic import BaseModel, field_validator, model_validator, EmailStr
from app.utils.role_enum import RoleEnum
from typing import Optional


class AdminVerificationIn(BaseModel):
    group_id: int
