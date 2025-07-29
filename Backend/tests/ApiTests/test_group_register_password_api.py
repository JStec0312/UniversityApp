def test_verify_admin_using_group_register_password_api(client, db_session, basic_seed):
    basic_seed()
    from datetime import datetime, timedelta
    # Login as a superior admin
    login_data = {
        "email": "admin@gmail.com",
        "password": "password"
    }
    from app.utils.timebox import Clock
    expiration_time = Clock.now() + timedelta(days=1)

    response_login = client.post("/api/user/admin/auth", json=login_data)
    assert response_login.status_code == 200
    print("Login response:", response_login.json())
    token = response_login.json().get("access_token")
    client.cookies.set("access_token", token)
    # Create atests/ApiTests/test_group_register_password_api.py group register password
    group_register_password_data = {
        "group_id": 2,
        "expires_at": expiration_time.isoformat(),  # Ensure the date is in ISO format
    }
    response_create_password = client.post("/api/user/superior-group/generate-group-password", json=group_register_password_data)
    assert response_create_password.status_code == 200
    assert response_create_password.json().get("group_id") == 2
    group_register_password = response_create_password.json().get("token")
    client.cookies.delete("access_token")
    
    
    from app.models.user import User
    user_id = db_session.query(User).filter(User.email == "nonverified@gmail.com").first().id

    import os
    from datetime import datetime, timedelta
    from jose import jwt
    SECRET_KEY = os.getenv("JWT_SECRET")
    data = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(minutes=60)  
    }
    verification_token = jwt.encode(data, SECRET_KEY, algorithm="HS256")

    response_verify_admin = client.post(f"/api/user/admin/verify/{verification_token}", json={
        "group_id":2,
        "group_password": group_register_password,
        })

    
    # Debug the response if it's not 200
    if response_verify_admin.status_code != 200:
        print(f"Error Status Code: {response_verify_admin.status_code}")
        print(f"Error Response: {response_verify_admin.json()}")
    
    assert response_verify_admin.status_code == 200

    data = response_verify_admin.json()
    
    login_data = {
        "email": "nonverified@gmail.com",
        "password": "password"
    }
    response_login = client.post("/api/user/admin/auth", json=login_data)
    from app.models.admin import Admin
    admin = db_session.query(Admin).filter(Admin.user_id == user_id).first()
    assert admin is not None
    assert response_login.status_code == 200
    token = response_login.json().get("access_token")
    print("Access Token:")
    print(token)
    
    client.cookies.set("access_token", token)
    response_me = client.get("/api/user/admin/me")
    assert response_me.status_code == 200

    