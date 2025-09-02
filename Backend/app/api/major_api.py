from fastapi import APIRouter, Depends
from app.schemas.major import MajorOut
from app.services.major_service import MajorService
from app.services.service_factory import get_major_service

router = APIRouter()

@router.get("/get-majors-by-faculty-id/{faculty_id}", response_model=list[MajorOut])
def get_faculties_by_university_id(
    faculty_id: int,
    major_service: MajorService = Depends(get_major_service),
):
    return major_service.get_majors_by_faculty_id(faculty_id=faculty_id)
