"""
Test module for admin API endpoints.

This module contains tests for admin authentication and verification endpoints.
Each test uses its own isolated database.
"""

def test_authenticate_admin(client, seed_admin):
    seed_admin()
    response = client.post("/api/user/admin/auth", json={
        "email": "test@gmail.com",
        "password": "testpassword",
    })
    assert response.status_code == 200
    
    # Test invalid email
    response = client.post("/api/user/admin/auth", json={
        "email": "stest@gmail.com",  # intentionally wrong email
        "password": "testpassword",
    })
    assert response.status_code == 401
    
    # Test invalid password
    response = client.post("/api/user/admin/auth", json={
        "email": "test@gmail.com",
        "password": "wrongpassword",  # intentionally wrong password
    })
    assert response.status_code == 401
    


def test_admin_me(client, seed_admin):
    seed_admin()
    # Register a new admin user
    login_response = client.post("/api/user/admin/auth", json={
        "email": "test@gmail.com",
        "password": "testpassword",
        })
    assert login_response.status_code == 200
    token = login_response.json().get("access_token")
    client.cookies.set("access_token", token)
    
    response_me = client.get("/api/user/admin/me")
    assert response_me.status_code == 200
    response_data = response_me.json()
    assert response_data["email"] == "test@gmail.com"
    assert response_data["role"] == "admin"
    assert response_data["display_name"] == "Admin User"
    assert response_data["university_id"] == 1  # Assuming university_id is 1 in seed_admin
    assert response_data["group_id"] == 1
    assert response_data["user_id"] == 1

def test_admin_me_unauthorized(client, basic_seed):
    basic_seed()
    # Attempt to access admin me endpoint without authentication
    response_me = client.get("/api/user/admin/me")
    assert response_me.status_code == 401
    
    #login as student
    response_auth = client.post("/api/user/student/auth", json={
        "email": "user@gmail.com",
        "password": "password",
    })
    assert response_auth.status_code == 200

    # Attempt to access admin me endpoint as student
    response_me = client.get("/api/user/admin/me")
    assert response_me.status_code == 403  # Forbidden, as student cannot access admin endpoint
    


def test_create_event(client, seed_admin, db_session):
    seed_admin()
    # Register a new admin user
    login_response = client.post("/api/user/admin/auth", json={
        "email": "test@gmail.com",
        "password": "testpassword",
        })
    assert login_response.status_code == 200
    # Create a new event
    response_event = client.post("/api/user/admin/event", json={
        "title": "Test Event",
        "description": "This is a test event",
        "start_date": "2027-08-24T14:30",
        "end_date": "2029-10-01T12:00",
        "location": "Test Location",
        "image_url": "http://example.com/image.jpg",
    })
    assert response_event.status_code == 200
    response_data = response_event.json()
    from app.models.event import Event
    event = db_session.query(Event).filter(Event.title == "Test Event").first()
    assert event is not None
    assert event.title == "Test Event"
    assert event.description == "This is a test event"
    import datetime
    assert event.start_date == datetime.datetime(2027, 8, 24, 14, 30)
    assert event.end_date == datetime.datetime(2029, 10, 1, 12, 0)
    assert event.location == "Test Location"
    assert event.university_id == 1  # Assuming university_id is 1 in seed_admin


def test_create_event_unauthorized(client, basic_seed):
    basic_seed()
    # Attempt to create an event without authentication
    response_event = client.post("/api/user/admin/event", json={
        "title": "Test Event",
        "description": "This is a test event",
        "start_date": "2025-07-24T14:30",
        "end_date": "2029-10-01T12:00",
        "location": "Test Location",
        "image_url": "http://example.com/image.jpg",
    })
    assert response_event.status_code == 401
    
    #login as student
    response_auth = client.post("/api/user/student/auth", json={
        "email": "user@gmail.com",
        "password": "password"
    })
    assert response_auth.status_code == 200
    # Attempt to create an event as student
    response_event = client.post("/api/user/admin/event", json={
        "title": "Test Event",
        "description": "This is a test event",
        "start_date": "2025-07-24T14:30",
        "end_date": "2029-10-01T12:00",
        "location": "Test Location",
        "image_url": "http://example.com/image.jpg",
    })
    assert response_event.status_code == 403  # Forbidden, as student cannot access admin endpoint
    