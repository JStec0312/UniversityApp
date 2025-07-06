
def test_get_group_register_password(client, basic_seed, db_session):
    """
    verified superior group admin credentiials: admin@gmail.com, password
    """
    basic_seed()
    response_auth = client.post("/api/user/admin/auth", json={
        "email": "admin@gmail.com",
        "password": "password",
    })
    assert response_auth.status_code == 200 
    token = response_auth.json().get("access_token")
    payload = {
        "group_name": "Test Group",
        "expires_at": "2030-12-31T23:59:59Z"   # ISO 8601 + strefa
    }
    headers = {"Authorization": f"Bearer {token}"}

    response_add_group = client.post("/api/user/superior-group/register-group", json=payload, headers=headers)
    

    assert response_add_group.status_code == 200
    response_data = response_add_group.json()
    assert response_data["group_name"] == "Test Group"

    #unatuhorized admin
    response_auth = client.post("/api/user/admin/auth", json={
        "email": "nonsuperior@gmail.com",
        "password": "password",
    })
    assert response_auth.status_code == 200 
    token = response_auth.json().get("access_token")
    payload = {
        "group_name": "Test Group",
        "expires_at": "2030-12-31T23:59:59Z"   # ISO 8601 + strefa
    }
    headers = {"Authorization": f"Bearer {token}"}

    response_add_group = client.post("/api/user/superior-group/register-group", json=payload, headers=headers)

    assert response_add_group.status_code == 403

    #unauthorized student
    response_auth = client.post("/api/user/student/auth", json={
        "email": "user@gmail.com",
        "password": "password",
    })
    assert response_auth.status_code == 200 
    token = response_auth.json().get("access_token")
    payload = {
        "group_name": "Test Group",
        "expires_at": "2030-12-31T23:59:59Z"   # ISO 8601 + strefa
    }
    headers = {"Authorization": f"Bearer {token}"}

    response_add_group = client.post("/api/user/superior-group/register-group", json=payload, headers=headers)

    assert response_add_group.status_code == 403

