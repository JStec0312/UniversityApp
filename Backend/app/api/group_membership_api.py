# app/api/group_membership_api.py (lub aktualna ścieżka pliku)
from fastapi import APIRouter, Depends, Query
from app.schemas.group_invite import GroupInviteCreate, GroupInviteOut
from app.schemas.admin import AdminOut
from app.schemas.group_member import (
    GroupMemberOut,
    GroupMemberOutDisplayName,
    GroupAdminCreate,
)
from app.utils.security.require import require
from app.services.group_membership_service import GroupMembershipService
from app.services.service_factory import get_group_membership_service

router = APIRouter()

# @router.get("/{group_id}/invitations", response_model=list[GroupInviteOut], status_code=200)
# def get_group_invitations(
#     group_id: int,
#     user = require.all,
#     svc: GroupMembershipService = Depends(get_group_membership_service),
# ):
#     return svc.get_group_invitations(group_id=group_id)

@router.post("/{group_id}/invitations", response_model=GroupInviteOut, status_code=201)
def invite_to_group(
    group_id: int,
    invite_data: GroupInviteCreate,  # invited_user_id (+ ewentualnie expires_at)
    user = require.admin_or_superior,  # globalny guard; szczegółowy check w serwisie
    svc: GroupMembershipService = Depends(get_group_membership_service),
):
    return svc.invite_user_to_group(
        invited_user_id=invite_data.invited_user_id,
        inviter_user_id=user["user_id"],
        group_id=group_id,
    )

@router.post("/invitations/{invitation_id}/accept", response_model=GroupMemberOut, status_code=200)
def accept_invite(
    invitation_id: int,
    user = require.all,
    svc: GroupMembershipService = Depends(get_group_membership_service),
):
    return svc.accept_group_invitation(invitation_id=invitation_id, user_id=user["user_id"])

@router.get("/{group_id}/members", response_model=list[GroupMemberOutDisplayName], status_code=200)
def get_group_members(
    group_id: int,
    user = require.all,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    svc: GroupMembershipService = Depends(get_group_membership_service),
):
    return svc.get_group_members(
        group_id=group_id,
        university_id=user["university_id"],
        limit=limit,
        offset=offset,
    )

@router.post("/{group_id}/admin", response_model=AdminOut, status_code=201)
def make_user_admin(
    group_id: int,
    admin_data: GroupAdminCreate,
    user = require.admin_or_superior,
    svc: GroupMembershipService = Depends(get_group_membership_service),
):
    return svc.add_group_admin(
        group_id=group_id,
        invited_user_id=admin_data.invited_user_id,
        inviter_user_id=user["user_id"],
    )
