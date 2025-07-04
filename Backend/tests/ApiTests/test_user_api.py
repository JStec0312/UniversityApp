from app.models import User, Student, Admin
def test_create_user(client):
    response = client.post("/api/users/", json={
        "email": "teseeet@example.com",
        "password": "testpassword",
        "display_name": "Test User",
        "university_id": "1"
    })


    assert response.status_code == 200
    data = response.json()
    assert data["display_name"] == "Test User"



def test_verify_student(client, test_data):
    db= test_data
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
    

    response_verify_student = client.post(f"/api/users/verify/student/{registered_user_token}", json=json_data_verify_student)
    assert response_verify_student.status_code == 200

    user = db.query(User).filter(User.id == response_register.json()["id"]).first()
    assert user.verified is True
    student = db.query(Student).filter(Student.user_id == user.id).first()
    assert student is not None
    assert student.faculty_id == json_data_verify_student["faculty_id"]
    admin = db.query(Admin).filter(Admin.user_id == user.id).first()
    assert admin is None
    

def test_verify_admin(client, test_data):
    db = test_data
    json_data_register = {
        "email": "test@gmail.com",
        "password": "testpassword",
        "display_name": "Test User",
        "university_id": 1
    }

    json_data_verify_admin = {
        "group_id": 1
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
    response_verify_admin = client.post(f"/api/users/verify/admin/{registered_user_token}", json=json_data_verify_admin)
    assert response_verify_admin.status_code == 200
    user = db.query(User).filter(User.id == response_register.json()["id"]).first()
    assert user.verified is True
    admin = db.query(Admin).filter(Admin.user_id == user.id).first()
    assert admin is not None
    assert admin.group_id == json_data_verify_admin["group_id"]
    student = db.query(Student).filter(Student.user_id == user.id).first()
    assert student is None


