from sqlalchemy.orm import Session
from sqlalchemy import delete

from app.repositories.base_repository import BaseRepository
from app.models.group import Group

class GroupRepository(BaseRepository[Group]):
    def __init__(self, session: Session):
        super().__init__(session, Group)

    def get_by_name(self, name: str, university_id: int) -> Group | None:
        return (
            self.session.query(self.model)
            .filter(
                self.model.group_name == name,
                self.model.university_id == university_id,
            )
            .first()
        )

    def get_by_university_id(self, university_id: int) -> list[Group]:
        return (
            self.session.query(self.model)
            .filter(self.model.university_id == university_id)
            .all()
        )

    def delete_by_id_and_university(self, group_id: int, university_id: int) -> int:
        """
        Usuwa grupę w ramach aktualnej transakcji (bez commit).
        Zwraca 1, jeśli coś usunięto, inaczej 0.
        """
        stmt = (
            delete(self.model)
            .where(self.model.id == group_id, self.model.university_id == university_id)
            .returning(self.model.id)
        )
        result = self.session.execute(stmt)
        deleted_id = result.scalar_one_or_none()
        # brak commit/rollback tutaj — transakcją zarządza warstwa serwisu
        return 1 if deleted_id is not None else 0
