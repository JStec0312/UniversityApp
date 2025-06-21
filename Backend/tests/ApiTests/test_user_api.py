
def test_create_user(client):
    response = client.post("/api/users/", json={
        "email": "teseeet@example.com",
        "password": "testpassword",
        "display_name": "Test User"
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
        "display_name": "Test User"
    })
    assert response.status_code == 200
    user_id = response.json()["id"]
    getResponse = client.get(f"/api/users/{user_id}")
    assert getResponse.status_code == 200
    data = getResponse.json()
    assert data["email"] == "test@example.com"
    assert data["display_name"] == "Test User"

