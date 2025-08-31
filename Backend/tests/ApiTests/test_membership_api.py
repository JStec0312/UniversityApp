def test_full_membership_test(client, sc_with_student_admin_and_superior_admin, auth, db_session):
    # Arrange
    scenario = sc_with_student_admin_and_superior_admin

    user_student, password_student = scenario["user_student"]
    user_admin, password_admin = scenario["user_admin"]
    user_superior_admin, password_superior_admin = scenario["user_superior_admin"]
    group = scenario["group"]

    #invite user to group
    auth.login_via_endpoint(client, email=user_admin.email, password=password_admin)

    response_group_invite = client.post(f"/api/group/{group.id}/invitations", json = {
        "invited_user_id": user_student.id,
    })
    assert response_group_invite.status_code == 201
    invite_id = response_group_invite.json().get("id")
    assert invite_id is not None
    auth.logout_via_endpoint(client)

    #accept invitation
    auth.login_via_endpoint(client, email=user_student.email, password=password_student)

    response_accept_invite = client.post(f"/api/group/invitations/{invite_id}/accept")
    assert response_accept_invite.status_code == 200

    #check if user is now a member of the group
    from app.models.group_member import GroupMember
    db_session.query(GroupMember).filter(GroupMember.user_id == user_student.id, GroupMember.group_id == group.id).one()

def test_invite_user_to_group_no_permission(client, sc_with_student_admin_and_superior_admin, auth):
    # Arrange
    scenario = sc_with_student_admin_and_superior_admin

    user_student, password_student = scenario["user_student"]
    user_admin, password_admin = scenario["user_admin"]
    user_superior_admin, password_superior_admin = scenario["user_superior_admin"]
    group = scenario["group"]

    # Try to invite user to group as a regular user
    auth.login_via_endpoint(client, email=user_student.email, password=password_student)

    response_group_invite = client.post(f"/api/group/{group.id}/invitations", json={
        "invited_user_id": user_student.id,
    })
    assert response_group_invite.status_code == 403


