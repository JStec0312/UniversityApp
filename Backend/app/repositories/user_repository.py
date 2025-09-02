from typing import List, Optional
from sqlalchemy.orm import Session, joinedload

from app.models.user import User
from app.models.student import Student
from app.repositories.base_repository import BaseRepository
from app.repositories.student_repository import StudentRepository

class UserRepository(BaseRepository[User]):
    def __init__(self, session: Session):
        super().__init__(session, User)

    def get_by_email(self, email: str) -> Optional[User]:
        return (
            self.session.query(User)
            .options(joinedload(User.student), joinedload(User.admin))
            .filter(User.email == email)
            .one_or_none()
        )

    def get_by_username(self, username: str) -> List[User]:
        return (
            self.session.query(self.model)
            .filter(self.model.display_name == username)
            .all()
        )

    def verify_user(self, id: int) -> Optional[User]:
        """
        Ustawia verified=True bez commit/refresh — transakcją zarządza serwis.
        """
        user = self.get_by_id(id, for_update=True)
        if not user:
            return None
        user.verified = True
        self.session.flush()
        return user

    def create_student(self, user_id: int, faculty_id: int | None = None, major_id: int | None = None) -> Student:
        """
        Tworzy rekord Student powiązany z istniejącym Userem.
        Zwraca utworzony obiekt Student. Bez commit — robi to warstwa serwisu.
        """
        existing_user = self.get_by_id(user_id, for_update=True)
        if not existing_user:
            raise ValueError("User does not exist")

        student_repo = StudentRepository(self.session)
        student = Student(
            user_id=user_id,
            faculty_id=faculty_id,
            major_id=major_id,
        )
        return student_repo.create(student)
