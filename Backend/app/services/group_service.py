from fastapi import HTTPException
from app.models.group import Group
from app.schemas.group import GroupCreateIn, GroupCreateOut, GroupByUniOut
from app.repositories.repository_factory import RepositoryFactory
from app.repositories.group_repository import GroupRepository
class GroupService:
    def __init__(self, group_repo):
        self.group_repo : GroupRepository = group_repo

    def create_group(self, data: GroupCreateIn, given_by):
        user_id = given_by
        user_repo = RepositoryFactory(self.group_repo.db).get_user_repository()
        university_id = user_repo.get_university_id_by_user_id(user_id)
        if not university_id:
            raise HTTPException(status_code=404, detail="University not found for the user")
        
        existing_group = self.group_repo.get_by_name(data.group_name, university_id)
        if existing_group:
            raise HTTPException(status_code=400, detail="Group with this name already exists in the university")
        
        group = self.group_repo.create(
            Group(
                group_name=data.group_name,
                university_id=university_id,
            )
        )

        if not group:
            raise HTTPException(status_code=500, detail="Failed to create group")
        
        return GroupCreateOut(
            group_id=group.id,
            group_name=group.group_name,
            university_id=group.university_id
        )
    
    def get_groups_by_university_id(self, university_id: int):
        groups = self.group_repo.getPaginatedWithConditions(
            conditions=(Group.university_id == university_id,),
            offset=0,
            limit=None
        )
        if not groups:
            raise HTTPException(status_code=404, detail="No groups found for this university")
        
        return [
            GroupByUniOut(
                group_id=group.id,
                group_name=group.group_name,
                university_id=group.university_id
            )
            for group in groups]
        
