
from app.schemas.admin import  AdminAuthIn, AdminAuthOut
from app.repositories.admin_repository import AdminRepository
from app.utils.role_enum import RoleEnum
from fastapi import HTTPException
from passlib.hash import bcrypt
from jose import jwt,JWTError


class AdminService:
    def __init__(self, admin_repo: AdminRepository):
        self.admin_repo = admin_repo

    def authenticate_admin(self, admin_auth):
        """
        Authenticate an admin using the provided authentication information.
        """
        # Logic to authenticate the admin
        admin = self.admin_repo.get_by_email(admin_auth.email)
        if not admin or not bcrypt.verify(admin_auth.password, admin.user.hashed_password):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )
        if not admin.user.verified:
            raise HTTPException(status_code=403, detail="User not verified")
        
        admin_access_token = jwt.encode({"sub": str(admin.user.id)}, "your_secret_key", algorithm="HS256")

        return AdminAuthOut(
            access_token=admin_access_token,
            token_type='bearer',
            role=RoleEnum.ADMIN ,
            admin_id=admin.id,
            user_id=admin.user_id,
            university_id=admin.user.university_id,
            email=admin.user.email,
            display_name=admin.user.display_name,
            group_id=admin.group_id
        )