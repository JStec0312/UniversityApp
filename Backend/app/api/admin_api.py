# app/api/admin_api.py
from fastapi import APIRouter, Depends
from app.schemas.event import AddEventIn
from app.utils.security.require_roles import require_roles
from app.utils.enums.role_enum import RoleEnum
from app.services.admin_service import AdminService
from app.services.service_factory import get_admin_service

# Create router instance for admin endpoints
router = APIRouter()

@router.post("/event")
def create_event(
    event_data: AddEventIn,
    admin_service: AdminService = Depends(get_admin_service),
    user = Depends(require_roles([RoleEnum.ADMIN.value, RoleEnum.SUPERIOR_ADMIN.value])),
):
    return admin_service.create_event(event_data, user["user_id"], user["university_id"])
