# app/api/university_api.py
from fastapi import APIRouter, Depends
from app.schemas.university import UniversityOut
from app.services.university_service import UniversityService
from app.services.service_factory import get_university_service

router = APIRouter()

@router.get("/get-universities", response_model=list[UniversityOut])
def get_universities(
    svc: UniversityService = Depends(get_university_service),
):
    return svc.get_all_universities()
