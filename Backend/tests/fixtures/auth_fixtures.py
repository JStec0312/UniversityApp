"""
Authentication and login helper fixtures.
"""
import pytest


@pytest.fixture
def superior_admin_login_on_base_seed(client, basic_seed):
    """Logs in a superior admin using basic seed data."""
    def _seed():
        basic_seed()
        response = client.post("/api/user/admin/auth", json={
            "email": "admin@gmail.com",
            "password": "password"
        })
        return response
    return _seed

@pytest.fixture
def student_login_on_base_seed(client, basic_seed):
    """Logs in a student using basic seed data."""
    def _seed():
        basic_seed()
        response = client.post("/api/user/student/auth", json={
            "email": "user@gmail.com",
            "password": "password"
        })
        return response
    return _seed