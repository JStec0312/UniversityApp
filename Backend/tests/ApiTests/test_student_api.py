
def test_authenticate_student(client, student_seed, db_session):   
    seed = student_seed() 
    response = client.post("/api/user/student/auth", json={"email": "test@gmail.com", "password": "testpassword"},
)
    assert response.status_code == 200
    
    # Test invalid email
    response = client.post("/api/user/student/auth", json={
        "email": "tstr@gmail.com",  # Invalid email
        "password": "testpassword",  # Correct password
    })
    assert response.status_code == 401
    
    # Test invalid password
    response = client.post("/api/user/student/auth", json={
        "email": "test@gmail.com",  # Correct email
        "password": "wrongpassword",  # Invalid password
    })
    assert response.status_code == 401
    
    # Test unverified account
    from app.models.user import User
    db_session.query(User).filter(User.email == "test@gmail.com").update({"verified": False})
    db_session.commit()
    response = client.post("/api/user/student/auth", json={
        "email": "test@gmail.com",  # Correct email
        "password": "testpassword",  # Correct password
    })
    assert response.status_code == 403


def test_student_me(client, student_seed, db_session):
    seed = student_seed()
    from app.models.user import User
    response_login = client.post("/api/user/student/auth", json={
        "email": "test@gmail.com",  # Correct email
        "password": "testpassword",  # Correct password
    })
    assert response_login.status_code == 200

    token = response_login.json()["access_token"]

    response_me = client.get("/api/user/student/me", headers={"Authorization": f"Bearer {token}"})
    assert response_me.status_code == 200
    data = response_me.json()
    assert data["role"] == "student"
    assert data["email"] == "test@gmail.com"
    assert data["display_name"] == "Test User"
    assert data["faculty_id"] == 1
    assert data["major_id"] == 1
    assert data["university_id"] == 1  
