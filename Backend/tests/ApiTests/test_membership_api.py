from app.models.group_member import GroupMember


def test_full_membership_test(client, sc_with_student_admin_and_superior_admin, auth, db_session):
    # Arrange
    scenario = sc_with_student_admin_and_superior_admin

    user_student, password_student = scenario["user_student"]
    user_admin, password_admin = scenario["user_admin"]
    user_superior_admin, password_superior_admin = scenario["user_superior_admin"]
    group = scenario["group"]

    #invite user to group
    auth.login_via_endpoint(client, email=user_admin.email, password=password_admin)

    response_group_invite = client.post(f"/api/groups/{group.id}/invitations", json = {
        "invited_user_id": user_student.id,
    })
    assert response_group_invite.status_code == 201
    invite_id = response_group_invite.json().get("id")
    assert invite_id is not None
    auth.logout_via_endpoint(client)

    #accept invitation
    auth.login_via_endpoint(client, email=user_student.email, password=password_student)

    response_accept_invite = client.post(f"/api/groups/invitations/{invite_id}/accept")
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

    response_group_invite = client.post(f"/api/groups/{group.id}/invitations", json={
        "invited_user_id": user_student.id,
    })
    assert response_group_invite.status_code == 403

def test_see_group_members(client, sc_with_student_admin_and_superior_admin, auth, db_session):
    scenario = sc_with_student_admin_and_superior_admin
    member1, password1 = scenario["user_admin"]
    member2, password2 = scenario["user_superior_admin"]
    non_member, password3 = scenario["user_student"]
    group = scenario["group"]
    auth.login_via_endpoint(client, email=non_member.email, password=password3)

    

    response_see_members = client.get(f"/api/groups/{group.id}/members")
    assert response_see_members.status_code == 200
    members = response_see_members.json()
    got_user_ids = {m["user_id"] for m in members}
    expected_user_ids = {member1.id, member2.id}
    assert got_user_ids == expected_user_ids
    assert len(members) == 2
    

def test_see_group_admins(client, sc_with_student_admin_and_superior_admin, auth):
    scenario = sc_with_student_admin_and_superior_admin
    member1, password1 = scenario["user_admin"]
    member2, password2 = scenario["user_superior_admin"]
    non_member, password3 = scenario["user_student"]
    group = scenario["group"]
    auth.login_via_endpoint(client, email=non_member.email, password=password3)

    response_see_admins = client.get(f"/api/groups/{group.id}/admins")
    assert response_see_admins.status_code == 200
    admins = response_see_admins.json()
    got_user_ids = {a["user_id"] for a in admins}
    expected_user_ids = {member1.id, member2.id}
    assert got_user_ids == expected_user_ids
    assert len(admins) == 2



def test_make_user_admin_no_permission(client, sc_with_student_admin_and_superior_admin, auth):
    # Arrange
    scenario = sc_with_student_admin_and_superior_admin

    user_student, password_student = scenario["user_student"]
    user_admin, password_admin = scenario["user_admin"]
    user_superior_admin, password_superior_admin = scenario["user_superior_admin"]
    group = scenario["group"]

    # Try to make user admin as a regular user
    auth.login_via_endpoint(client, email=user_student.email, password=password_student)

    response_make_admin = client.post(f"/api/groups/{group.id}/admins", json={
        "invited_user_id": user_student.id,
    })
    assert response_make_admin.status_code == 403


def test_make_user_admin_with_permission(client, sc_with_student_admin_and_superior_admin, auth, db_session):
    # Arrange
    scenario = sc_with_student_admin_and_superior_admin

    user_student, password_student = scenario["user_student"]
    user_admin, password_admin = scenario["user_admin"]
    user_superior_admin, password_superior_admin = scenario["user_superior_admin"]
    group = scenario["group"]

    # Make user admin as a superior admin
    auth.login_via_endpoint(client, email=user_superior_admin.email, password=password_superior_admin)

    response_make_admin = client.post(f"/api/groups/{group.id}/admins", json={
        "invited_user_id": user_student.id,
    })
    assert response_make_admin.status_code == 201

    #check if the user is now an admin
    response_see_admins = client.get(f"/api/groups/{group.id}/admins")
    assert response_see_admins.status_code == 200
    admins = response_see_admins.json()
    got_user_ids = {a["user_id"] for a in admins}
    expected_user_ids = {user_admin.id, user_superior_admin.id, user_student.id}
    assert got_user_ids == expected_user_ids
    assert len(admins) == 3