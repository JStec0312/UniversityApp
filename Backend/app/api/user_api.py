# app/api/user_api.py

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.user import UserCreate, UserOut
from app.repositories.repository_factory import RepositoryFactory
from app.services.service_factory import ServiceFactory
from app.utils.require_roles import require_roles
from app.utils.role_enum import RoleEnum

router = APIRouter()


@router.post("/", response_model=UserOut)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    user_repo = RepositoryFactory(db).get_user_repository()
    user_service = ServiceFactory.get_user_service(user_repo)
    return user_service.create_user(user_in)


@router.post("/getToken/{user_id}")
def get_verification_token(user_id: int, db: Session = Depends(get_db)):
    user_repo = RepositoryFactory(db).get_user_repository()
    user_service = ServiceFactory.get_user_service(user_repo)
    return user_service.get_verification_token(user_id)    

@router.get("/getEmail", response_model=str)
def get_user_email(db: Session = Depends(get_db), user = Depends(require_roles([RoleEnum.ADMIN.value, RoleEnum.SUPERIOR_ADMIN.value, RoleEnum.STUDENT.value]))):
    user_repo = RepositoryFactory(db).get_user_repository()
    user_service = ServiceFactory.get_user_service(user_repo)
    return user_service.get_user_email(user["user_id"])