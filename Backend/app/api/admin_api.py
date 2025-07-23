
"""
Admin API endpoints for authentication and verification of admin users.
This module provides routes for admin authentication and verification.
"""

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.repositories.repository_factory import RepositoryFactory
from app.services.service_factory import ServiceFactory
from app.schemas.admin import AdminVerificationIn, AdminAuthIn, AdminAuthOut, AdminMeOut
from app.schemas.user import UserOut
from app.utils.require_roles import require_roles
from app.utils.role_enum import RoleEnum
from app.schemas.event import AddEventIn

# Create router instance for admin endpoints
router = APIRouter()

@router.post("/admin/verify/{token}", response_model=UserOut)
def verify_admin(token: str, verification_info: AdminVerificationIn, db: Session = Depends(get_db)):
    """
    Verify an admin user account using the provided verification token.
    
    Args:
        token: The verification token sent to the admin's email
        verification_info: Additional verification information
        db: Database session dependency
        
    Returns:
        UserOut: The verified user information
    """
    user_repo = RepositoryFactory(db).get_user_repository()
    user_service = ServiceFactory.get_user_service(user_repo)
    return user_service.verify_admin(token, verification_info)

@router.post("/admin/auth", response_model=AdminAuthOut)
def authenticate_admin(admin_auth: AdminAuthIn, response:Response, db: Session = Depends(get_db)):
    """
    Authenticate an admin user and generate an access token.
    
    Args:
        admin_auth: Admin authentication credentials (email and password)
        db: Database session dependency
        
    Returns:
        AdminAuthOut: Authentication response with access token and admin information
    """
    admin_repo = RepositoryFactory(db).get_admin_repository()
    admin_service = ServiceFactory.get_admin_service(admin_repo)
    return admin_service.authenticate_admin(admin_auth, response)


@router.get("/admin/me", response_model=AdminMeOut)
def get_current_admin(db: Session = Depends(get_db), user = Depends(require_roles([RoleEnum.ADMIN.value, RoleEnum.SUPERIOR_ADMIN.value]))):
    """
    Get the current authenticated student.
    
    This endpoint retrieves the details of the currently authenticated student.
    
    Returns:
        UserOut: The details of the authenticated student.
    """
    admin_repo = RepositoryFactory(db).get_admin_repository()
    admin_service = ServiceFactory.get_admin_service(admin_repo)
    return admin_service.get_current_admin(user["user_id"])

@router.post("/admin/event")
def create_event(event_data: AddEventIn, db:Session = Depends(get_db), user = Depends(require_roles([RoleEnum.ADMIN.value, RoleEnum.SUPERIOR_ADMIN.value]))):
    """
    Create a new event as an admin.
    
    This endpoint allows an admin to create a new event.
    
    Args:
        event_data: The data for the new event.
        db: Database session dependency.
        
    Returns:
        EventOut: Status code indicating success or failure.
    """
    admin_repo = RepositoryFactory(db).get_admin_repository()
    admin_service = ServiceFactory.get_admin_service(admin_repo)
    return admin_service.create_event(event_data, user["user_id"])