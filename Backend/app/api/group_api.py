
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.utils.security.require_roles import require_roles
from app.utils.role_enum import RoleEnum
from app.schemas.group import  GroupByUniOut
from app.repositories.repository_factory import RepositoryFactory
from app.services.service_factory import ServiceFactory

router = APIRouter()
@router.get("/get-groups-from-university", response_model=list[GroupByUniOut])
def get_groups_by_university_id( db: Session = Depends(get_db), user: dict = Depends(require_roles([ RoleEnum.ADMIN.value, RoleEnum.SUPERIOR_ADMIN.value, RoleEnum.STUDENT.value]))):
    group_repo = RepositoryFactory(db).get_group_repository()
    group_service = ServiceFactory.get_group_service(group_repo)
    return group_service.get_groups_by_university_id(university_id=user["university_id"])
