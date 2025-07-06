from app.schemas.student import StudentAuthIn, StudentAuthOut, StudentOut, StudentMeOut
from app.repositories.student_repository import StudentRepository
from fastapi import HTTPException
from passlib.hash import bcrypt
from jose import jwt,JWTError
from datetime import datetime, timedelta

from app.utils.role_enum import RoleEnum

import os
SECRET_KEY = os.getenv("JWT_SECRET")

class StudentService:
    def __init__(self, student_repo: StudentRepository ):
        self.student_repo = student_repo

    def authenticate_student(self, student_auth: StudentAuthIn ) -> StudentAuthOut:
        student = self.student_repo.get_by_email(student_auth.email)
        if not student or not bcrypt.verify(student_auth.password, student.user.hashed_password):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )
        if not student.user.verified:
            raise HTTPException(status_code=403, detail="User not verified")
        
        student_access_token = jwt.encode({"sub": str(student.user.id), "role": RoleEnum.STUDENT.value, "exp":datetime.now() + timedelta(hours=1) }, SECRET_KEY, algorithm="HS256")

        return StudentAuthOut(
            access_token = student_access_token, 
            token_type= 'bearer',
            student = StudentOut(
                student_id = student.id,
                user_id = student.user_id,
                university_id= student.user.university_id,
                email = student.user.email,
                faculty_id= student.faculty_id,
                major_id= student.major_id,
                display_name= student.user.display_name
            )
        )
    
    def get_current_student(self, user_id: int):
        student = self.student_repo.get_by_user_id(user_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        return StudentMeOut(
            role = RoleEnum.STUDENT,
            user_id = student.user_id,
            email = student.user.email,
            display_name = student.user.display_name,
            faculty_id = student.faculty_id,
            major_id = student.major_id,
            university_id = student.user.university_id
        )
    

    