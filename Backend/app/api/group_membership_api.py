from typing import Annotated
from fastapi import APIRouter, Depends, Query, Response, Request, BackgroundTasks
from app.services.service_factory import ServiceFactory
from app.repositories.repository_factory import RepositoryFactory
from app.schemas.group_invite import GroupInviteCreate, GroupInviteOut
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.utils.security.require import require


router  = APIRouter()
DBSession = Annotated[Session, Depends(get_db)]

@router.post("/{group_id}/invitations", response_model=GroupInviteOut, status_code=201)
def invite_to_group(
    group_id: int,
    invite_data: GroupInviteCreate,  # zawiera tylko: invited_user_id (+ ewentualnie expires_at)
    db: DBSession,
    user = require.admin_or_superior,  # globalny guard; szczegółowy check w serwisie
):
    rf = RepositoryFactory(db)
    sf = ServiceFactory()
    svc = sf.get_group_membership_service(
        group_members_repo=rf.get_group_member_repository(),
        group_invite_repo=rf.get_group_invitation_repository(),
        user_repository=rf.get_user_repository(),
        admin_repository=rf.get_admin_repository(),
        group_repository=rf.get_group_repository(),  # potrzebny do 404 na grupie
    )
    inv = svc.invite_user_to_group(
        invited_user_id=invite_data.invited_user_id,
        inviter_user_id=user["user_id"],
        group_id=group_id,
        expires_at=getattr(invite_data, "expires_at", None),
    )
    return inv