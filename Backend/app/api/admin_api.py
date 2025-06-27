
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.repositories.repository_factory import RepositoryFactory
from app.services.service_factory import ServiceFactory
from app.schemas.admin import  AdminVerificationIn, AdminAuthIn, AdminAuthOut
from app.schemas.user import UserOut

router = APIRouter()

@router.post("/verify/admin/{token}", response_model = UserOut)
def verify_admin(token: str, verification_info: AdminVerificationIn,  db: Session = Depends(get_db)):
    user_repo = RepositoryFactory(db).get_user_repository()
    user_service = ServiceFactory.get_user_service(user_repo)
    return user_service.verify_admin(token, verification_info)

@router.post("/admin/auth", response_model = AdminAuthOut)
def authenticate_admin(admin_auth: AdminAuthIn, db: Session = Depends(get_db)):
    admin_repo = RepositoryFactory(db).get_admin_repository()
    admin_service = ServiceFactory.get_admin_service(admin_repo)
    return admin_service.authenticate_admin(admin_auth)

