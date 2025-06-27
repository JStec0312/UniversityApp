from sqlalchemy.orm import Session
from app.models.student import Student
from app.models.user import User
from app.repositories.base_repository import BaseRepository

class StudentRepository(BaseRepository[Student]):
    def __init__(self, db: Session):
        super().__init__(db, Student)

    def get_by_user_id(self, user_id: int) -> Student | None:
        return self.db.query(self.model).filter(
            self.model.user_id == user_id
        ).first()

    def get_by_university_id(self, university_id: int) -> list[Student]:
        return self.db.query(self.model).filter(
            self.model.university_id == university_id
        ).all()
    
    def get_by_major_id(self, major_id: int) -> list[Student]:
        return self.db.query(self.model).filter(
            self.model.major_id == major_id
        ).all()
    def get_by_faculty_id(self, faculty_id: int) -> list[Student]:
        return self.db.query(self.model).filter(
            self.model.faculty_id == faculty_id
        ).all()
    
    def get_by_email(self, email: str):
        return (
            self.db.query(Student)
            .join(Student.user)  
            .filter(User.email == email)
            .first()
        )