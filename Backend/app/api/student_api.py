from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.repositories.repository_factory import RepositoryFactory
from app.services.service_factory import ServiceFactory
from app.schemas.student import StudentVerificationIn, StudentAuthOut, StudentAuthIn
from app.schemas.user import UserOut
router = APIRouter()

@router.post("/verify/student/{token}", response_model=UserOut)
def verify_user(token: str, verification_info: StudentVerificationIn,  db: Session = Depends(get_db)):
    user_repo = RepositoryFactory(db).get_user_repository()
    user_service = ServiceFactory.get_user_service(user_repo)
    return user_service.verify_student(token, verification_info)



@router.post("/student/auth", response_model = StudentAuthOut)
def authenticate_user(user_auth: StudentAuthIn, db: Session = Depends(get_db)):
    student_repo = RepositoryFactory(db).get_student_repository()
    student_service = ServiceFactory.get_student_service(student_repo)
    return student_service.authenticate_student(user_auth)