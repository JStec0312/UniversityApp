# app/api/faculty_api.py
from fastapi import APIRouter, Depends
from app.schemas.faculty import FacultyOut
from app.services.faculty_service import FacultyService
from app.services.service_factory import get_faculty_service

router = APIRouter()

@router.get("/get-faculties-by-uni-id/{university_id}", response_model=list[FacultyOut])
def get_faculties_by_university_id(
    university_id: int,
    faculty_service: FacultyService = Depends(get_faculty_service),
):
    return faculty_service.get_faculties_by_university_id(university_id)
