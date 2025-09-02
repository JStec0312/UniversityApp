from sqlalchemy.orm import Session
from app.models.major import Major
from app.repositories.base_repository import BaseRepository

class MajorRepository(BaseRepository[Major]):
    def __init__(self, session: Session):
        super().__init__(session, Major)

    def get_by_name(self, name: str, university_id: int) -> Major | None:
        return (
            self.session.query(self.model)
            .filter(
                self.model.name == name,
                self.model.university_id == university_id,
            )
            .first()
        )

    def get_by_university_id(self, university_id: int) -> list[Major]:
        return (
            self.session.query(self.model)
            .filter(self.model.university_id == university_id)
            .all()
        )
    
    def get_by_faculty_id(self, faculty_id: int) -> list[Major]:
        return (
            self.session.query(self.model)
            .filter(self.model.faculty_id == faculty_id)
            .all()
        )
