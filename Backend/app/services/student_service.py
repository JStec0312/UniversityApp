from datetime import datetime, timedelta, timezone  # jeśli gdzieś indziej używane
import os
from jose import jwt, JWTError, ExpiredSignatureError
from sqlalchemy.exc import IntegrityError

from app.models.student import Student
from app.models.user import User
from app.repositories.student_repository import StudentRepository
from app.repositories.faculty_repository import FacultyRepository
from app.repositories.major_repository import MajorRepository
from app.repositories.user_repository import UserRepository
from app.utils.uow import uow
from app.core.service_errors import (
    UserNotVerifiedException,                     # (nieużywany tutaj, ale pewnie potrzebny gdzie indziej)
    FacultyDoesNotBelongToUniversityException,
    InvalidCredentialsException,                  # (jw.)
    InvalidVerificationTokenException,
    UserAlreadyVerifiedException,
    MajorDoesNotBelongToFacultyException,
    UserNotFoundException,
    InvalidInputException,                        # (jw.)
)

SECRET_KEY = os.getenv("JWT_SECRET")

class StudentService:
    def __init__(
        self,
        student_repo: StudentRepository,
        faculty_repo: FacultyRepository | None = None,
        major_repo: MajorRepository | None = None,
        user_repo: UserRepository | None = None,
    ):
        self.student_repo = student_repo
        self.faculty_repo = faculty_repo
        self.major_repo = major_repo
        self.user_repo = user_repo
        self.session = student_repo.session  # jedna sesja do transakcji

    def verify_student(self, token: str, faculty_id: int | None, major_id: int | None) -> User:
        # 1) token -> user_id
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = int(payload["sub"])
        except (ExpiredSignatureError, JWTError, KeyError, ValueError):
            raise InvalidVerificationTokenException("Invalid verification token")

        # 2) użytkownik
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundException("User not found")
        if user.verified:
            raise UserAlreadyVerifiedException("User already verified")

        expected_university_id = user.university_id

        # 3) walidacje fakultet/kierunek
        major = None
        if major_id:
            if not self.major_repo:
                # jeśli repo nie wstrzyknięto, nie mamy jak zweryfikować
                raise InvalidInputException("Major repository is not available")
            major = self.major_repo.get_by_id(major_id)
            if not major:

                raise MajorDoesNotBelongToFacultyException("Major does not belong to the faculty")
            if not faculty_id:
                faculty_id = major.faculty_id

        faculty = None
        if faculty_id:
            if not self.faculty_repo:
                raise InvalidInputException("Faculty repository is not available")
            faculty = self.faculty_repo.get_by_id(faculty_id)

        if faculty and faculty.university_id != expected_university_id:
            raise FacultyDoesNotBelongToUniversityException("Faculty does not belong to the university")
        if major and faculty and major.faculty_id != faculty.id:
            raise MajorDoesNotBelongToFacultyException("Major does not belong to the faculty")

        try:
            with uow(self.session):
                self.student_repo.create(Student(
                    user_id=user.id,
                    faculty_id=faculty_id,   # może być None
                    major_id=major_id,       # może być None
                ))
                self.user_repo.verify_user(user.id)
            return user
        except IntegrityError:
            raise UserAlreadyVerifiedException("User already verified")
