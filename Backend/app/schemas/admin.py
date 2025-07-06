"""
Admin schema module for request and response validation.

This module provides Pydantic models for validating admin-related
request bodies and response data.
"""

from pydantic import BaseModel, field_validator, model_validator, EmailStr
from app.utils.role_enum import RoleEnum
from typing import Optional


class AdminOut(BaseModel):
    admin_id: int
    university_id: int
    user_id: int
    email: EmailStr
    display_name: str
    group_id: int

class AdminVerificationIn(BaseModel):
    """
    Schema for admin verification request.
    
    This model is used when verifying an admin account, requiring
    the group ID that the admin belongs to.
    
    Attributes:
        group_id: ID of the group the admin belongs to
    """
    group_id: int


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
    """
    Schema for admin authentication response.
    
    This model defines the structure of the response when an admin
    successfully authenticates, including the JWT token and admin details.
    
    Attributes:
        access_token: JWT token for authenticated requests
        token_type: Type of token (typically "bearer")
        role: Admin role enum value
        admin_id: ID of the admin record
        university_id: ID of the university the admin belongs to
        user_id: ID of the user record associated with the admin
        email: Admin's email address
        display_name: Admin's display name
        group_id: ID of the group the admin belongs to
    """
    access_token: str
    token_type: str = "bearer"
    admin: AdminOut
    

class AdminMeOut(BaseModel):
    role : RoleEnum = RoleEnum.ADMIN
    user_id: int
    email: EmailStr
    display_name: str
    group_id: int
    university_id: int
    