def test_authenticate_admin(client, admin_data):
    db = admin_data
    response = client.post("/api/users/admin/auth", json={
        "email": "test@gmail.com",  # added in conftest.py
        "password": "testpassword",  # added in conftest.py
    })
    assert response.status_code == 200

def test_authenticate_admin_invalid_email(client, admin_data):
    db = admin_data
    response = client.post("/api/users/admin/auth", json={
        "email": "stest@gmail.com",  # intentionally wrong email
        "password": "testpassword",  # added in conftest.py
    })
    assert response.status_code == 401

def test_authenticate_admin_invalid_password(client, admin_data):
    db = admin_data
    response = client.post("/api/users/admin/auth", json={
        "email": "test@gmail.com",
        "password": "wrongpassword",  # intentionally wrong password
    })
    assert response.status_code == 401

def test_authenticate_admin_unverified_user(client, admin_data):
    db = admin_data
    # Set the user to unverified
    from app.models.user import User

    user = db.query(User).filter(User.email == "test@gmail.com").first()
    user.verified = False
    db.commit()
    response = client.post("/api/users/admin/auth", json={
        "email": "test@gmail.com",
        "password": "testpassword",  # added in conftest.py
    })
    assert response.status_code == 403
