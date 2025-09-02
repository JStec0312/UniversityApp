# app/services/service_factory.py
"""
Service providers for FastAPI DI (preferred) + thin compatibility shim.

Uzywaj get_*_service w routerach:
    from fastapi import Depends
    from app.services.service_factory import get_group_membership_service

    def handler(..., svc: GroupMembershipService = Depends(get_group_membership_service), ...):
        ...
"""

from typing import Optional
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.db import get_db

# Services
from app.services.event_service import EventService
from app.services.group_service import GroupService
from app.services.news_service import NewsService
from app.services.student_service import StudentService
from app.services.user_service import UserService
from app.services.admin_service import AdminService
from app.services.university_service import UniversityService
from app.services.faculty_service import FacultyService
from app.services.major_service import MajorService
from app.services.group_membership_service import GroupMembershipService
from app.services.me_service import MeService

# Repositories
from app.repositories.group_invitation_repository import GroupInvitationRepository
from app.repositories.group_member_repository import GroupMemberRepository
from app.repositories.user_repository import UserRepository
from app.repositories.admin_repository import AdminRepository
from app.repositories.group_repository import GroupRepository
from app.repositories.event_repository import EventRepository
from app.repositories.student_repository import StudentRepository

# Opcjonalne repo (jesli masz)
try:
    from app.repositories.university_repository import UniversityRepository
except Exception:
    UniversityRepository = None  # type: ignore
try:
    from app.repositories.faculty_repository import FacultyRepository
except Exception:
    FacultyRepository = None  # type: ignore
try:
    from app.repositories.major_repository import MajorRepository
except Exception:
    MajorRepository = None  # type: ignore
try:
    from app.repositories.news_repository import NewsRepository
except Exception:
    NewsRepository = None  # type: ignore


# -------- PREFERRED: DI providers --------

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db))

def get_student_service(db: Session = Depends(get_db)) -> StudentService:
    faculty_repo = FacultyRepository(db) if FacultyRepository else None
    major_repo = MajorRepository(db) if MajorRepository else None
    student_repo = StudentRepository(db) if StudentRepository else None
    user_repo = UserRepository(db) if UserRepository else None
    return StudentService(faculty_repo=faculty_repo, major_repo=major_repo, student_repo=student_repo, user_repo=user_repo)

def get_admin_service(db: Session = Depends(get_db)) -> AdminService:
    # jesli masz dedykowany AdminRepository dla AdminService, podmien tutaj
    return AdminService(UserRepository(db))

def get_university_service(db: Session = Depends(get_db)) -> UniversityService:
    if not UniversityRepository:
        raise RuntimeError("UniversityRepository not available")
    return UniversityService(UniversityRepository(db))

def get_faculty_service(db: Session = Depends(get_db)) -> FacultyService:
    if not FacultyRepository:
        raise RuntimeError("FacultyRepository not available")
    return FacultyService(FacultyRepository(db))

def get_major_service(db: Session = Depends(get_db)) -> MajorService:
    if not MajorRepository:
        raise RuntimeError("MajorRepository not available")
    return MajorService(MajorRepository(db))

def get_group_service(db: Session = Depends(get_db)) -> GroupService:
    return GroupService(GroupRepository(db))

def get_event_service(db: Session = Depends(get_db)) -> EventService:
    return EventService(EventRepository(db))

def get_news_service(db: Session = Depends(get_db)) -> NewsService:
    if not NewsRepository:
        raise RuntimeError("NewsRepository not available")
    return NewsService(NewsRepository(db))

def get_group_membership_service(db: Session = Depends(get_db)) -> GroupMembershipService:
    return GroupMembershipService(
        GroupMemberRepository(db),
        GroupInvitationRepository(db),
        UserRepository(db),
        AdminRepository(db),
        GroupRepository(db),
    )

def get_me_service(db: Session = Depends(get_db)) -> MeService:
    return MeService(
        UserRepository(db),
        GroupRepository(db),
        EventRepository(db),
        AdminRepository(db),
        StudentRepository(db),
        GroupMemberRepository(db),
        GroupInvitationRepository(db),
    )


__all__ = [
    # DI providers
    "get_user_service",
    "get_student_service",
    "get_admin_service",
    "get_university_service",
    "get_faculty_service",
    "get_major_service",
    "get_group_service",
    "get_event_service",
    "get_news_service",
    "get_group_membership_service",
    "get_me_service",
]


