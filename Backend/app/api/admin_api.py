

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.repositories.repository_factory import RepositoryFactory
from app.services.service_factory import ServiceFactory
from app.schemas.admin import AdminVerificationIn, AdminAuthIn, AdminAuthOut, AdminMeOut
from app.schemas.user import UserOut
from app.utils.security.require_roles import require_roles
from app.utils.role_enum import RoleEnum
from app.schemas.event import AddEventIn

# Create router instance for admin endpoints
router = APIRouter()


@router.post("/event")
def create_event(event_data: AddEventIn, db:Session = Depends(get_db), user = Depends(require_roles([RoleEnum.ADMIN.value, RoleEnum.SUPERIOR_ADMIN.value]))):
    admin_repo = RepositoryFactory(db).get_admin_repository()
    admin_service = ServiceFactory.get_admin_service(admin_repo)
    return admin_service.create_event(event_data, user["user_id"], user["university_id"])