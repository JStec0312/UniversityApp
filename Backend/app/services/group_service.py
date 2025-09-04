from sqlalchemy.exc import IntegrityError

from app.models.group import Group
from app.schemas.group import GroupCreateIn
from app.core.service_errors import (
    GroupAlreadyExistsError,
    GroupHasDependenciesError,
    GroupNotFoundError,
)
from app.repositories.group_repository import GroupRepository
from app.utils.uow import uow

class GroupService:
    def __init__(self, group_repo: GroupRepository):
        self.group_repo: GroupRepository = group_repo
        self.session = group_repo.session  # jedna sesja/UoW

    def create_group(self, data: GroupCreateIn, university_id: int) -> Group:
        try:
            with uow(self.session):
                return self.group_repo.create(
                    Group(group_name=data.group_name, university_id=university_id)
                )
        except IntegrityError as e:
            raise GroupAlreadyExistsError("Group with this name already exists") from e

    def get_groups_by_university_id(self, university_id: int, limit: int, offset: int) -> list[Group]:
        groups = self.group_repo.get_paginated_with_conditions(
            conditions=(Group.university_id == university_id,),
            offset=offset,
            limit=limit,
        )
        if not groups:
            raise GroupNotFoundError("No groups found for this university")
        return groups

    def delete_group(self, group_id: int, university_id: int) -> None:
        try:
            with uow(self.session):
                deleted_count = self.group_repo.delete_by_id_and_university(group_id, university_id)
        except IntegrityError as err:
            raise GroupHasDependenciesError(
                "Group has dependencies and cannot be deleted"
            ) from err

        if deleted_count == 0:
            raise GroupNotFoundError(
                "Group not found or does not belong to the specified university"
            )
