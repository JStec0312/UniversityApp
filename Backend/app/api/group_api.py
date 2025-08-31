
from app.models import Group
from typing import Annotated
from app.schemas.group import  GroupByUniOut
from app.repositories.repository_factory import RepositoryFactory
from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.services.service_factory import ServiceFactory
from app.utils.security.require import require
from app.schemas.group import GroupCreateIn, GroupCreateOut


router = APIRouter()
DBSession = Annotated[Session, Depends(get_db)]

@router.get("/", response_model=list[GroupByUniOut])
def get_groups_by_university_id(
    db: DBSession,
    user: dict = require.all,
    limit:int = Query(default=20, ge=1, le=100),
    offset:int = Query(default=0, ge=0),
    ):
    group_repo = RepositoryFactory(db).get_group_repository()
    group_service = ServiceFactory.get_group_service(group_repo)
    groups = group_service.get_groups_by_university_id(university_id=user["university_id"], limit=limit, offset=offset)
    return groups


@router.post("/", response_model=GroupCreateOut, status_code = 201)
def create_group(data: GroupCreateIn, db: DBSession, user = require.superior):
    group_repo = RepositoryFactory(db).get_group_repository()
    group_service = ServiceFactory.get_group_service(group_repo)
    group = group_service.create_group(data=data, university_id=user["university_id"])
    return group


@router.delete("/{group_id}", status_code=204)
def delete_group(group_id: int, db: DBSession, user = require.superior):
    group_repo = RepositoryFactory(db).get_group_repository()
    group_service = ServiceFactory.get_group_service(group_repo)
    group_service.delete_group(group_id=group_id, university_id=user["university_id"])

@router.get("/groups/{group_id}", response_model=GroupByUniOut)
def get_group(group_id: int, db: DBSession, user = require.all):
    group_repo = RepositoryFactory(db).get_group_repository()
    group_service = ServiceFactory.get_group_service(group_repo)
    group = group_service.get_group(group_id=group_id, university_id=user["university_id"])
    return group