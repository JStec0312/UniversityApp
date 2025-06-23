from app.models import User, Student, Admin
def test_create_user(client):
    response = client.post("/api/users/", json={
        "email": "teseeet@example.com",
        "password": "testpassword",
        "display_name": "Test User",
        "university_id": "1"
    })

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.json())

    assert response.status_code == 200
    data = response.json()
    assert data["display_name"] == "Test User"

def test_get_user(client):
    # First create a user
    response = client.post("/api/users/", json={
        "email": "test@example.com",
        "password": "testpassword",
        "display_name": "Test User",
        "university_id": "1"
    })
    assert response.status_code == 200
    user_id = response.json()["id"]
    getResponse = client.get(f"/api/users/{user_id}")
    assert getResponse.status_code == 200
    data = getResponse.json()
    assert data["email"] == "test@example.com"
    assert data["display_name"] == "Test User"

def test_verify_student(client, test_data):
    db= test_data
    json_data_register = {
        "email": "test@gmail.com",
        "password": "testpassword",
        "display_name": "Test User",
        "verified": False,
        "university_id": 1
    }
    
    json_data_verify_student = {
        "role": "student",
        "faculty_id": 1,
        "major_id": 1
    }

    
    response_register = client.post("/api/users/", json=json_data_register)
    assert response_register.status_code == 200

    from jose import jwt 
    from datetime import datetime, timedelta
    import os
    
    SECRET_KEY = os.getenv("JWT_SECRET")

    registered_user_token = jwt.encode({
        "sub": str(response_register.json()["id"]),
        "exp": datetime.utcnow() + timedelta(minutes=60)  
    }, SECRET_KEY, algorithm="HS256")
    
    response_verify_student = client.post(f"/api/users/verify/{registered_user_token}", json=json_data_verify_student)
    print("Verify Student Response:", response_verify_student.json())
    assert response_verify_student.status_code == 200

    user = db.query(User).filter(User.id == response_register.json()["id"]).first()
    assert user.verified is True
    student = db.query(Student).filter(Student.user_id == user.id).first()
    assert student is not None
    assert student.faculty_id == json_data_verify_student["faculty_id"]
    admin = db.query(Admin).filter(Admin.user_id == user.id).first()
    assert admin is None
    

    

    

    

    
    
    