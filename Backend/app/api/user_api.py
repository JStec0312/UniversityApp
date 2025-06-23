# app/api/user_api.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.user import UserCreate, UserOut, VerificationInfoIn
from app.repositories.repository_factory import RepositoryFactory
from app.services.user_service import UserService
router = APIRouter()


@router.post("/", response_model=UserOut)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    user_repo = RepositoryFactory(db).get_user_repository()
    user_service = UserService(user_repo)
    return user_service.create_user(user_in)

@router.post("/verify/{token}", response_model=UserOut)
def verify_user(token: str, verification_info: VerificationInfoIn,  db: Session = Depends(get_db)):
    user_repo = RepositoryFactory(db).get_user_repository()
    user_service = UserService(user_repo)
    return user_service.verify_user(token, verification_info)

@router.post("/getToken/{user_id}")
def get_verification_token(user_id: int, db: Session = Depends(get_db)):
    user_repo = RepositoryFactory(db).get_user_repository()
    user_service = UserService(user_repo)
    return user_service.get_verification_token(user_id)    
