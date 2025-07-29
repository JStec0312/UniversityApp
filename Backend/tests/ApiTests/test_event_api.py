
def test_see_events(client, event_api_seed):
    event_api_seed()
    #login
    response = client.post("/api/user/student/auth", json={
        "email": "test@gmail.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    
    response_see_events = client.get("/api/event/upcoming")
    assert response_see_events.status_code == 200
    events = response_see_events.json()
    assert len(events) == 1
    

def test_see_events_unauthorized(client):
    response = client.get("/api/event/upcoming")
    assert response.status_code == 401
    
