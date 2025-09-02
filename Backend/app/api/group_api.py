# app/api/group_api.py
from fastapi import APIRouter, Depends, Query

from app.schemas.group import GroupByUniOut, GroupCreateIn, GroupCreateOut
from app.utils.security.require import require
from app.services.group_service import GroupService
from app.services.service_factory import get_group_service

router = APIRouter()

@router.get("/", response_model=list[GroupByUniOut])
def get_groups_by_university_id(
    group_service: GroupService = Depends(get_group_service),
    user: dict = require.all,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    return group_service.get_groups_by_university_id(
        university_id=user["university_id"], limit=limit, offset=offset
    )

@router.post("/", response_model=GroupCreateOut, status_code=201)
def create_group(
    data: GroupCreateIn,
    group_service: GroupService = Depends(get_group_service),
    user = require.superior,
):
    return group_service.create_group(data=data, university_id=user["university_id"])

@router.delete("/{group_id}", status_code=204)
def delete_group(
    group_id: int,
    group_service: GroupService = Depends(get_group_service),
    user = require.superior,
):
    group_service.delete_group(group_id=group_id, university_id=user["university_id"])

@router.get("/groups/{group_id}", response_model=GroupByUniOut)
def get_group(
    group_id: int,
    group_service: GroupService = Depends(get_group_service),
    user = require.all,
):
    return group_service.get_group(group_id=group_id, university_id=user["university_id"])
