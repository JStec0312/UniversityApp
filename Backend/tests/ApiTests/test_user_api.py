"""
Test module for user API endpoints.

This module contains tests for user creation, student verification, and admin verification.
Each test uses its own isolated database.
"""
import os
from sqlalchemy import create_engine
from app.main import app
from app.core.db import Base, get_db
from tests.RepositoryTest import test_user




def test_create_verify_and_login_as_user(client, user_seed):
    user_seed = user_seed()
    user_data = {
        "email":"test@gmail.com",
        "password" : "testpassword",
        "university_id": 1,
        "display_name" : "test_user",        
    }
    #register
    register_response = client.post("/api/user", json={
        "email": user_data["email"],
        "password": user_data["password"],
        "university_id": user_data["university_id"],
        "display_name": user_data["display_name"]
    })
    assert register_response.status_code == 201
    assert register_response.json()["id"] == 1

    from app.utils.security.jwt_tokens import create_verify_token
    token = create_verify_token(int(register_response.json()["id"]))

    #verify
    verify_response = client.post("/api/user/student/verify", json={"token": token})
    assert verify_response.status_code == 200


    #login
    login_response = client.post("/api/user/login", json={
        "email": user_data["email"],
        "password": user_data["password"]
    })
    assert login_response.status_code == 200
    

def test_get_email(client, basic_seed):
    basic_seed = basic_seed()
    response_login = client.post("/api/user/student/auth", json={
        "email": "user@gmail.com",
        "password": "password"
    })
    assert response_login.status_code == 200
    response = client.get("/api/user/email")
    assert response.status_code == 200
    assert response.json() == {'email': 'user@gmail.com'}



def test_search_users(client, superior_admin_login_on_base_seed ):
    superior_admin_login_on_base_seed()
    response = client.get("/api/user/search", params={"name": "Test User"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_user(client, superior_admin_login_on_base_seed):   
    superior_admin_login_on_base_seed()
    response = client.get("/api/user/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

