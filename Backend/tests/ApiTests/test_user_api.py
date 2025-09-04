
from app.models.user import User


def test_create_verify_and_login_as_user(client, sc_no_users, db_session):
    scenario = sc_no_users
    user_data = {
        "email":"test@gmail.com",
        "password" : "testpassword",
        "university_id": scenario["university"].id,
        "display_name" : "test_user",        
    }
    #register
    register_response = client.post("/api/users", json={
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
    verify_response = client.post("/api/users/students/verify", json={"token": token})
    assert verify_response.status_code == 200


    #login
    login_response = client.post("/api/users/login", json={
        "email": user_data["email"],
        "password": user_data["password"]
    })
    assert login_response.status_code == 200
    

def test_get_email(client, sc_with_verified_user_student, auth):
    scenario = sc_with_verified_user_student
    user, password = scenario["user"]
    client =  auth.login_via_endpoint(client, email=user.email, password=password)
    assert client.cookies.get("access_token") is not None, "No access token in cookies" #tutaj przechodzi
    response = client.get("/api/users/email")
    assert response.status_code == 200
    assert response.json() == {'email': user.email}



def test_search_users(client,  sc_with_verified_user_student , auth):
    scenario = sc_with_verified_user_student
    user, password = scenario["user"]
    client =  auth.login_via_endpoint(client, email=user.email, password=password)

    response = client.get("/api/users/search", params={"name": "Test User"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_user(client, sc_with_verified_user_student, auth):   
    scenario = sc_with_verified_user_student
    user, password = scenario["user"]
    client =  auth.login_via_endpoint(client, email=user.email, password=password)

    response = client.get("/api/users/1")
    assert response.status_code == 200
    assert response.json()["id"] == user.id
    assert response.json()["display_name"] == user.display_name
    
    

