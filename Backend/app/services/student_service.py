from app.schemas.student import StudentAuthIn, StudentAuthOut, StudentOut, StudentMeOut
from app.repositories.student_repository import StudentRepository
from fastapi import HTTPException, Response
from fastapi.responses import JSONResponse
from passlib.hash import bcrypt
from jose import jwt,JWTError
from datetime import datetime, timedelta

from app.utils.role_enum import RoleEnum

import os
SECRET_KEY = os.getenv("JWT_SECRET")

class StudentService:
    def __init__(self, student_repo: StudentRepository ):
        self.student_repo = student_repo

    def authenticate_student(self, student_auth: StudentAuthIn, response: Response ) -> StudentAuthOut:
        student = self.student_repo.get_by_email(student_auth.email)
        
        if not student or not bcrypt.verify(student_auth.password, student.user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        if not student.user.verified:
            raise HTTPException(status_code=403, detail="User not verified")
        
        student_access_token = jwt.encode({"sub": str(student.user.id), "role": RoleEnum.STUDENT.value, "exp":datetime.now() + timedelta(hours=1) }, SECRET_KEY, algorithm="HS256")
        expires = datetime.now() + timedelta(hours=1)

        response.set_cookie(
            key="access_token",
            value=student_access_token,
            httponly=True,
            secure=False,              # ⚠️ tylko przez HTTPS – wyłącz na localhost jeśli trzeba
            max_age=60 * 60,          # 1h
            expires=expires.timestamp(),
            path="/"
        )
        return StudentAuthOut(
            student = StudentOut(
                student_id = student.id,
                user_id = student.user_id,
                university_id= student.user.university_id,
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
    


    def logout(self, response: Response):
        response = JSONResponse(content={"message": "Logged out successfully"}, status_code=200)
        response.delete_cookie("access_token", path="/")
        return response
