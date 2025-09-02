from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.student import Student
from app.models.user import User
from app.repositories.base_repository import BaseRepository

class StudentRepository(BaseRepository[Student]):
    def __init__(self, session: Session):
        super().__init__(session, Student)

    def get_by_user_id(self, user_id: int) -> Optional[Student]:
        return (
            self.session.query(self.model)
            .filter(self.model.user_id == user_id)
            .first()
        )

    def get_by_university_id(self, university_id: int) -> List[Student]:
        return (
            self.session.query(self.model)
            .filter(self.model.university_id == university_id)
            .all()
        )
    
    def get_by_major_id(self, major_id: int) -> List[Student]:
        return (
            self.session.query(self.model)
            .filter(self.model.major_id == major_id)
            .all()
        )

    def get_by_faculty_id(self, faculty_id: int) -> List[Student]:
        return (
            self.session.query(self.model)
            .filter(self.model.faculty_id == faculty_id)
            .all()
        )
    
    def get_by_email(self, email: str) -> Optional[Student]:
        return (
            self.session.query(self.model)
            .join(self.model.user)  # relacja Student.user
            .filter(User.email == email)
            .first()
        )

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return (
            self.session.query(User)
            .filter(User.id == user_id)
            .first()
        )
    
    def verify_user(self, user_id: int) -> None:
        """
        Ustawia verified=True bez commit — commitem zarządza warstwa serwisu.
        """
        user = self.get_user_by_id(user_id)
        if user:
            user.verified = True
            self.session.flush()
