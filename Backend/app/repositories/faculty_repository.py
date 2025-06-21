from sqlalchemy.orm import Session
from app.models.faculty import Faculty
from app.repositories.base_repository import BaseRepository

class FacultyRepository(BaseRepository[Faculty]):
    def __init__(self, db: Session):
        super().__init__(db, Faculty)

    def get_by_name(self, name: str, university_id) -> Faculty | None:
        return self.db.query(self.model).filter(
            self.model.name == name,
            self.model.university_id == university_id
        ).first()
    def get_by_university_id(self, university_id: int) -> list[Faculty]:
        return self.db.query(self.model).filter(
            self.model.university_id == university_id
        ).all()