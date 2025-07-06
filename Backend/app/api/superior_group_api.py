
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.repositories.repository_factory import RepositoryFactory
from app.services.service_factory import ServiceFactory
from app.schemas.group_register_password import GroupRegisterPasswordCreate, GroupRegisterPasswordOut
from app.utils.require_roles import require_roles
from app.utils.role_enum import RoleEnum
router = APIRouter()

@router.post("/register-group", response_model=GroupRegisterPasswordOut)
def create_group_register_password(data: GroupRegisterPasswordCreate, db: Session = Depends(get_db), user = Depends(require_roles([RoleEnum.SUPERIOR_ADMIN.value]))):
    group_register_password_repo = RepositoryFactory(db).get_group_register_password_repository()
    group_register_password_service = ServiceFactory.get_group_register_password_service(group_register_password_repo)
    return group_register_password_service.create_group_register_password(data = data, given_by= user["user_id"])