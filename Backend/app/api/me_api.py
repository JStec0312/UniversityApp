# app/api/routes/me.py
from typing import Optional
from fastapi import APIRouter, Depends, Query

from app.utils.enums.invitation_status_enum import InvitationStatus
from app.utils.security.require import require
from app.schemas.group_invite import GroupInviteOut
from app.services.me_service import MeService
from app.services.service_factory import get_me_service

router = APIRouter()

@router.get("/invitations", response_model=list[GroupInviteOut])
def get_group_invitations(
    svc: MeService = Depends(get_me_service),
    user = require.all,
    status: Optional[InvitationStatus] = Query(None),
    limit: Optional[int] = Query(50, ge=1, le=200),
    offset: Optional[int] = Query(0, ge=0),
):
    return svc.see_my_invitations(user["user_id"], limit=limit, offset=offset)
