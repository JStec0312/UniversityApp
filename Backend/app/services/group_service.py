from fastapi import HTTPException
from app.models.group import Group
from app.schemas.group import GroupCreateIn,  GroupByUniOut
from app.core.service_errors import GroupAlreadyExistsException, GroupHasDependenciesException, GroupNotFoundException
from sqlalchemy.exc import IntegrityError
from app.repositories.group_repository import GroupRepository
class GroupService:
    def __init__(self, group_repo):
        self.group_repo : GroupRepository = group_repo

    def create_group(self, data: GroupCreateIn, university_id:int):
    
        try:
            return  self.group_repo.create(Group(
                group_name=data.group_name,
                university_id=university_id
            ))
        except IntegrityError as e:
            raise GroupAlreadyExistsException("Group with this name already exists")
        


    def get_groups_by_university_id(self, university_id: int, limit: int, offset: int):
        groups = self.group_repo.get_paginated_with_conditions(
            conditions=(Group.university_id == university_id,),
            offset=offset,
            limit=limit
        )
        if not groups:
            raise GroupNotFoundException("No groups found for this university")
        
        return groups
    

    def delete_group(self, group_id: int, university_id: int):
        group = self.group_repo.get_by_id(group_id)
        if not group or group.university_id != university_id:
            raise GroupNotFoundException("Group not found or does not belong to this university")
        try:
            self.group_repo.delete_by_id(group_id)
        except IntegrityError as e:
            raise GroupHasDependenciesException("Group has dependencies and cannot be deleted")
