def test_authenticate_student(client, student_data):
    db = student_data
    response = client.post("/api/users/student/auth", json={
        "email": "test@gmail.com", #added in conftest.py
        "password": "testpassword", #added in conftest.py
    })
    assert response.status_code == 200 


