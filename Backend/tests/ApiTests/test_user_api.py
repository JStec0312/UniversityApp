"""
Test module for user API endpoints.

This module contains tests for user creation, student verification, and admin verification.
Each test uses its own isolated database.
"""
import os
from sqlalchemy import create_engine
from app.main import app
from app.core.db import Base, get_db
from app.models import User, University, Faculty, Major, Group, Admin, Student
from datetime import datetime, timedelta
from jose import jwt



def test_create_user(client, user_seed):
    response = client.post("/api/user/", json={
        "email": "teseeet@example.com",
        "password": "testpassword",
        "display_name": "Test User",
        "university_id": "1"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["display_name"] == "Test User"

def test_verify_student(client, user_seed, db_session):
    user_seed = user_seed()
    db  = db_session
    
    # Register a new user
    json_data_register = {
        "email": "test@gmail.com",
        "password": "testpassword",
        "display_name": "Test User",
        "university_id": 1
    }
    
    json_data_verify_student = {
        "faculty_id": 1,
        "major_id": 1
    }

    response_register = client.post("/api/user/", json=json_data_register)
    assert response_register.status_code == 200
    
    # Create verification token
    SECRET_KEY = os.getenv("JWT_SECRET", "your_secret_key")
    registered_user_token = jwt.encode({
        "sub": str(response_register.json()["id"]),
        "exp": datetime.utcnow() + timedelta(minutes=60)  
    }, SECRET_KEY, algorithm="HS256")
    
    # Verify student
    response_verify_student = client.post(
        f"/api/user/student/verify/{registered_user_token}", 
        json=json_data_verify_student
    )
    assert response_verify_student.status_code == 200

    # Check database records
    user = db.query(User).filter(User.id == response_register.json()["id"]).first()
    assert user.verified is True
    
    student = db.query(Student).filter(Student.user_id == user.id).first()
    assert student is not None
    assert student.faculty_id == json_data_verify_student["faculty_id"]
    
    admin = db.query(Admin).filter(Admin.user_id == user.id).first()
    assert admin is None



def test_get_email(client, basic_seed):
    basic_seed = basic_seed()
    response_login = client.post("/api/user/student/auth", json={
        "email": "user@gmail.com",
        "password": "password"
    })
    assert response_login.status_code == 200
    token = response_login.json().get("access_token")
    response = client.post("/api/user/getEmail")
    assert response.status_code == 200
    assert response.json() == "user@gmail.com"

