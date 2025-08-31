# app/api/routes/me.py
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.utils.enums.invitation_status_enum import InvitationStatus
from app.utils.security.require import require
from app.repositories.repository_factory import RepositoryFactory
from app.services.service_factory import ServiceFactory
from app.schemas.group_invite import GroupInviteOut

router = APIRouter()
DBSession = Annotated[Session, Depends(get_db)]

router.get("/invitations", response_model=list[GroupInviteOut])
def get_group_invitations(
        db: DBSession = DBSession, 
        user = require.all,
        status: Optional[InvitationStatus] = Query(None),
        limit: Optional[int] = Query(50, ge = 1, le = 200),
        offset: Optional[int] = Query(0, ge = 0),
        ):
    rf  = RepositoryFactory(db)
    svc = ServiceFactory.get_me_service(
        group_invitation_repository=rf.get_group_invitation_repository()
    )

    return svc.see_my_invitations(user["user_id"], limit=limit, offset=offset)