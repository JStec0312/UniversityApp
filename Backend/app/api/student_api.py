from fastapi import APIRouter, Depends

from app.schemas.student import StudentVerificationIn
from app.schemas.user import UserOut
from app.services.student_service import StudentService
from app.services.service_factory import get_student_service

router = APIRouter()

@router.post("/verify", response_model=UserOut)
def verify_student(
    body: StudentVerificationIn,
    svc: StudentService = Depends(get_student_service),
):
    return svc.verify_student(body.token, body.faculty_id, body.major_id)
