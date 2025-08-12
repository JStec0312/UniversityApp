from app.models.student import Student
from app.schemas.student import StudentAuthIn, StudentAuthOut,  StudentVerificationIn
from app.repositories.repository_factory import  StudentRepository, FacultyRepository, MajorRepository
from sqlalchemy.exc import IntegrityError
from passlib.hash import bcrypt
from jose import ExpiredSignatureError, jwt,JWTError
from datetime import datetime, timedelta, timezone
from app.exceptions.service_errors import UserNotVerifiedException,  FacultyDoesNotBelongToUniversityException, InvalidCredentialsException, InvalidVerificationTokenException, UserAlreadyVerifiedException, MajorDoesNotBelongToFacultyException, UserNotFoundException, InvalidInputException
from app.models import User

from app.utils.role_enum import RoleEnum

import os
SECRET_KEY = os.getenv("JWT_SECRET")

class StudentService:
    def __init__(self, student_repo: StudentRepository, faculty_repo: FacultyRepository = None, major_repo: MajorRepository = None):
        self.student_repo = student_repo
        self.faculty_repo = faculty_repo
        self.major_repo = major_repo

    
    def verify_student(self, token: str, faculty_id:int, major_id:int) -> User:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = int(payload["sub"])
        except (ExpiredSignatureError, JWTError, KeyError, ValueError):
            raise InvalidVerificationTokenException("Invalid verification token")

        # 2) user
        user = self.student_repo.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException("User not found")
        if user.verified:
            raise UserAlreadyVerifiedException("User already verified")

        expected_university_id = user.university_id

        major = self.major_repo.get_by_id(major_id) if major_id else None
        if not major and major_id:
            raise MajorDoesNotBelongToFacultyException("Major does not belong to the faculty")
        if major_id and not faculty_id:
            faculty_id = major.faculty_id

        faculty = self.faculty_repo.get_by_id(faculty_id) if faculty_id else None

        
        if faculty and faculty.university_id != expected_university_id:
            raise FacultyDoesNotBelongToUniversityException("Faculty does not belong to the university")
        if major and major.faculty_id != faculty.id:
            raise MajorDoesNotBelongToFacultyException("Major does not belong to the faculty")
        
        try:
            self.student_repo.create(Student(
                user_id=user.id,
                faculty_id=faculty_id,   # może być None
                major_id=major_id,       # może być None
            ))
            self.student_repo.verify_user(user.id)
        except IntegrityError:
            raise UserAlreadyVerifiedException("User already verified")

        self.student_repo.db.refresh(user)
        return user



    
    

