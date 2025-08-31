"""
Admin schema module for request and response validation.

This module provides Pydantic models for validating admin-related
request bodies and response data.
"""

from pydantic import BaseModel, field_validator, model_validator, EmailStr
from app.utils.enums.role_enum import RoleEnum
from typing import Optional


class AdminOut(BaseModel):
    admin_id: int
    university_id: int
    user_id: int
    display_name: str
    group_id: int
    group_name: str

class AdminVerificationIn(BaseModel):
    """
    Schema for admin verification request.
    
    This model is used when verifying an admin account, requiring
    the group ID that the admin belongs to.
    
    Attributes:
        group_id: ID of the group the admin belongs to
    """
    group_id: int
    group_password: str


class AdminAuthIn(BaseModel):
    """
    Schema for admin authentication request.
    
    This model validates the credentials provided when an admin
    attempts to log in.
    
    Attributes:
        email: Admin's email address
        password: Admin's password (plain text, will be verified against hashed version)
    """
    email: EmailStr
    password: str


class AdminAuthOut(BaseModel):

    admin: AdminOut

    

class AdminMeOut(BaseModel):
    role : RoleEnum = RoleEnum.ADMIN
    user_id: int
    email: EmailStr
    display_name: str
    group_id: int
    university_id: int
    