def test_full_membership_test(client, sc_with_student_admin_and_superior_admin, auth):
    scenario = sc_with_student_admin_and_superior_admin

    user_student, password_student = scenario["user_student"]
    user_admin, password_admin = scenario["user_admin"]
    user_superior_admin, password_superior_admin = scenario["user_superior_admin"]

    auth.login_via_endpoint(client, email=user_admin.email, password=password_admin)