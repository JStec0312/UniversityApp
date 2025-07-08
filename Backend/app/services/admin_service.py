
"""
Admin service module for handling admin-related business logic.

This module provides the AdminService class which implements authentication and other 
admin-specific functionality.
"""

from app.schemas.admin import AdminAuthIn, AdminAuthOut, AdminOut, AdminMeOut
from app.repositories.admin_repository import AdminRepository
from app.utils.role_enum import RoleEnum
from fastapi import HTTPException, Response
from passlib.hash import bcrypt
from jose import jwt, JWTError
from datetime import datetime, timedelta


import os
SECRET_KEY = os.getenv("JWT_SECRET")

class AdminService:
    """
    Service class for admin-related operations.
    
    This class handles business logic for admin users, including authentication,
    verification, and other admin-specific operations.
    """
    
    def __init__(self, admin_repo: AdminRepository):
        """
        Initialize the AdminService with a repository.
        
        Args:
            admin_repo: Repository for accessing admin data
        """
        self.admin_repo = admin_repo

    def authenticate_admin(self, admin_auth: AdminAuthIn, response: Response) -> AdminAuthOut:
     
        # Get admin by email
        admin = self.admin_repo.get_by_email(admin_auth.email)
        
        
        # Verify credentials
        if not admin or not bcrypt.verify(admin_auth.password, admin.user.hashed_password):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )
            
        # Check if user is verified
        if not admin.user.verified:
            raise HTTPException(status_code=403, detail="User not verified")
        
        role = RoleEnum.SUPERIOR_ADMIN if len(admin.group.superior_groups) > 0 else RoleEnum.ADMIN
        
        # Generate JWT token
        admin_access_token = jwt.encode({"sub": str(admin.user.id), "role":role.value, "exp": datetime.now() + timedelta(hours=1)}, SECRET_KEY, algorithm="HS256")
        
        response.set_cookie(
            key="access_token",
            value=admin_access_token,
            httponly=True,
            secure=False,  # ⚠️ only over HTTPS – disable on localhost if needed
            max_age=60 * 60,  # 1 hour
            expires=(datetime.now() + timedelta(hours=1)).timestamp(),
            path="/"
        )

        # Return authentication response
        return AdminAuthOut(
            admin = AdminOut(
                admin_id=admin.id,
                user_id=admin.user_id,
                university_id=admin.user.university_id,
                email=admin.user.email,
                display_name=admin.user.display_name,
                group_id=admin.group_id
            )
        )
    
    def get_current_admin(self, user_id: int) -> AdminMeOut:
        admin = self.admin_repo.get_by_user_id(user_id)
        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")
        return AdminMeOut(
            role=RoleEnum.ADMIN,
            user_id=admin.user_id,
            email=admin.user.email,
            display_name=admin.user.display_name,
            university_id=admin.user.university_id,
            group_id=admin.group_id
        )
    