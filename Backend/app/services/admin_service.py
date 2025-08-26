from app.core.service_errors import UserNotFoundException, UserAlreadyVerifiedException, InvalidVerificationTokenException, GroupNotFoundException, GroupNotBelongToUniversityException, InvalidGroupPasswordException
from app.schemas.admin import AdminAuthIn, AdminAuthOut, AdminOut, AdminMeOut, AdminVerificationIn
from app.repositories.admin_repository import AdminRepository
from app.models.user import User
from app.repositories.group_repository import GroupRepository
from app.repositories.user_repository import UserRepository
from app.utils.role_enum import RoleEnum
from fastapi import HTTPException
from passlib.hash import bcrypt
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta
from app.schemas.event import AddEventIn
from app.models.event import Event
from zoneinfo import ZoneInfo


import os
SECRET_KEY = os.getenv("JWT_SECRET")

class AdminService:


    def __init__(self, admin_repo: AdminRepository, group_repo: GroupRepository = None, user_repo: UserRepository = None):
        self.admin_repo = admin_repo
        self.group_repo = group_repo
        self.user_repo = user_repo

    



        
        
    
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


    def create_event(self, event_data: AddEventIn, user_id: int, university_id: int):
        event_repo = self.admin_repo.get_event_repository()
        group_id = self.admin_repo.get_group_id_by_user_id(user_id)
        

        if not group_id:
            raise HTTPException(status_code=404, detail="Group not found for user")

        start = event_data.start_date
        end = event_data.end_date
        now = datetime.now(ZoneInfo("Europe/Warsaw"))

        if start >= end:
            raise HTTPException(status_code=400, detail="Start date must be before end date")
        if start < now:
            raise HTTPException(status_code=400, detail="Start date cannot be in the past")

        new_event = Event(
            title=event_data.title,
            description=event_data.description,
            start_date=start,
            end_date=end,
            location=event_data.location,
            image_url=event_data.image_url,
            group_id=group_id, 
            university_id=university_id
        )

        event_repo.create(new_event)

        return {
            "status": "success",
            "message": "Event created successfully",
            "event_id": new_event.id
        }
