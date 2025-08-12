
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.repositories.repository_factory import RepositoryFactory
from app.services.service_factory import ServiceFactory
from app.utils.security.require_roles import require_roles
from app.utils.role_enum import RoleEnum
from app.schemas.group import GroupCreateIn, GroupCreateOut
router = APIRouter()

# @router.post("/generate-group-password", response_model=GroupRegisterPasswordOut)
# def create_group_register_password(data: GroupRegisterPasswordCreate, db: Session = Depends(get_db), user = Depends(require_roles([RoleEnum.SUPERIOR_ADMIN.value]))):
#     group_register_password_repo = RepositoryFactory(db).get_group_register_password_repository()
#     group_register_password_service = ServiceFactory.get_group_register_password_service(group_register_password_repo)
#     return group_register_password_service.create_group_register_password(data = data, given_by= user["user_id"])


# @router.post("/create-group", response_model = GroupCreateOut)
# def create_group(data: GroupCreateIn, db: Session = Depends(get_db), user = Depends(require_roles([RoleEnum.SUPERIOR_ADMIN.value]))):
#     group_repo = RepositoryFactory(db).get_group_repository()
#     group_service = ServiceFactory.get_group_service(group_repo)
#     return group_service.create_group(data = data, given_by= user["user_id"])