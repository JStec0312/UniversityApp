"""
Test module for admin API endpoints.

This module contains tests for admin authentication and verification endpoints.
Each test uses its own isolated database.
"""
from app.core.db import get_db

def test_authenticate_admin(client, seed_admin):
    seed_admin()
    response = client.post("/api/user/admin/auth", json={
        "email": "test@gmail.com",
        "password": "testpassword",
    })
    assert response.status_code == 200
    
    # Test invalid email
    response = client.post("/api/user/admin/auth", json={
        "email": "stest@gmail.com",  # intentionally wrong email
        "password": "testpassword",
    })
    assert response.status_code == 401
    
    # Test invalid password
    response = client.post("/api/user/admin/auth", json={
        "email": "test@gmail.com",
        "password": "wrongpassword",  # intentionally wrong password
    })
    assert response.status_code == 401
    


def test_admin_me(client, seed_admin):
    seed_admin()
    # Register a new admin user
    login_response = client.post("/api/user/admin/auth", json={
        "email": "test@gmail.com",
        "password": "testpassword",
        })
    assert login_response.status_code == 200
    token = login_response.json().get("access_token")
    client.cookies.set("access_token", token)
    
    response_me = client.get("/api/user/admin/me")
    assert response_me.status_code == 200
    response_data = response_me.json()
    assert response_data["email"] == "test@gmail.com"
    assert response_data["role"] == "admin"
    assert response_data["display_name"] == "Admin User"
    assert response_data["university_id"] == 1  # Assuming university_id is 1 in seed_admin
    assert response_data["group_id"] == 1
    assert response_data["user_id"] == 1

def test_admin_me_unauthorized(client, basic_seed):
    basic_seed()
    # Attempt to access admin me endpoint without authentication
    response_me = client.get("/api/user/admin/me")
    assert response_me.status_code == 401
    
    #login as student
    response_auth = client.post("/api/user/student/auth", json={
        "email": "user@gmail.com",
        "password": "password",
    })
    assert response_auth.status_code == 200
    token = response_auth.json().get("access_token")
    client.cookies.set("access_token", token)

    # Attempt to access admin me endpoint as student
    response_me = client.get("/api/user/admin/me")
    assert response_me.status_code == 403  # Forbidden, as student cannot access admin endpoint
    
 