from app.models.group import Group
def test_create_group(superior_group_api_seed, client, db_session):
    superior_group_api_seed()
    
    #login as a superior admin
    login_data = {
        "email": "test@gmail.com",
        "password": "testpassword"
    }
    response_login = client.post("/api/user/admin/auth", json=login_data)
    assert response_login.status_code == 200
    token = response_login.json().get("access_token")
    client.cookies.set("access_token", token)
    

    # Prepare the data for creating a group
    data = {
        "group_name": "New non superior group",
    }
    
    # Make the API call to create a group
    response = client.post("/api/user/superior-group/create-group", json=data)
    
    # Check if the response status code is 200 OK
    assert response.status_code == 200

    new_group_record = db_session.query(Group).filter(Group.group_name == "New non superior group").first()
    assert new_group_record is not None
    assert new_group_record.group_name == "New non superior group"
    assert new_group_record.university_id == 1  # Assuming university_id is 1
    assert new_group_record.id == response.json().get("group_id")

def test_create_group_unauthorized_admin(superior_group_api_seed, client):
    superior_group_api_seed()
    
    #login as a superior admin
    login_data = {
        "email": "test2@gmail.com",
        "password": "testpassword"
    }
    response_login = client.post("/api/user/admin/auth", json=login_data)
    assert response_login.status_code == 200
    token = response_login.json().get("access_token")
    client.cookies.set("access_token", token) 
    

    # Prepare the data for creating a group
    data = {
        "group_name": "New non superior group",
    }
    
    # Make the API call to create a group
    response = client.post("/api/user/superior-group/create-group", json=data)
    
    assert response.status_code == 403


def test_create_group_unauthorized_student(superior_group_api_seed, client):
    superior_group_api_seed()
    
    #login as a superior admin
    login_data = {
        "email": "test3@gmail.com",
        "password": "testpassword"
    }
    response_login = client.post("/api/user/student/auth", json=login_data)
    assert response_login.status_code == 200
    token = response_login.json().get("access_token")
    client.cookies.set("access_token", token) 
    

    # Prepare the data for creating a group
    data = {
        "group_name": "New non superior group",
    }
    
    # Make the API call to create a group
    response = client.post("/api/user/superior-group/create-group", json=data)
    
    assert response.status_code == 403


    