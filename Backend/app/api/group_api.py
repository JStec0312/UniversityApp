
from app.models import group
from app.schemas.group import  GroupByUniOut
from app.repositories.repository_factory import RepositoryFactory
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.exceptions.service_errors import GroupAlreadyExistsException, GroupHasDependenciesException, GroupNotFoundException
from app.repositories.repository_factory import RepositoryFactory
from app.services.service_factory import ServiceFactory
from app.utils.security.require import require
from app.schemas.group import GroupCreateIn, GroupCreateOut


router = APIRouter()
@router.get("/", response_model=list[GroupByUniOut])
def get_groups_by_university_id(
    db: Session = Depends(get_db), 
    user: dict = require.all,
    limit:int = Query(default=20, ge=1, le=100),
    offset:int = Query(default=0, ge=0),
    ):
    group_repo = RepositoryFactory(db).get_group_repository()
    group_service = ServiceFactory.get_group_service(group_repo)
    groups = group_service.get_groups_by_university_id(university_id=user["university_id"], limit=limit, offset=offset)
    return [GroupByUniOut(
        group_id=group.id,
        group_name=group.name,
        university_id=group.university_id
    ) for group in groups]


@router.post("/", response_model=GroupCreateOut, status_code = 201)
def create_group(data: GroupCreateIn, db:Session = Depends(get_db), user = require.superior):
    group_repo = RepositoryFactory(db).get_group_repository()
    group_service = ServiceFactory.get_group_service(group_repo)
    try:
        group = group_service.create_group(data = data, university_id = user["university_id"])
        return GroupCreateOut(
            group_id=group.id,
            group_name=group.name,
            university_id=user["university_id"]
        )
    except GroupAlreadyExistsException as e:
        raise HTTPException(status_code=409, detail=str(e))



@router.delete("/{group_id}", status_code=204)
def delete_group(group_id: int, db: Session = Depends(get_db), user = require.superior):
    group_repo = RepositoryFactory(db).get_group_repository()
    group_service = ServiceFactory.get_group_service(group_repo)
    try:
        group_service.delete_group(group_id=group_id, university_id=user["university_id"])
    except GroupNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except GroupHasDependenciesException as e:
        raise HTTPException(status_code=409, detail=str(e))