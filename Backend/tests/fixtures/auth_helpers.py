from datetime import datetime, timedelta, timezone
from http import client
from typing import Optional
from jose import jwt


LOGIN_PATH = "/api/user/login"

class Auth:
    
    def login_via_endpoint(self, client, *, email: str, password: str  ):
        response = client.post(LOGIN_PATH, json={"email": email, "password": password})
        assert response.status_code == 200
        assert client.cookies.get("access_token") is not None, "No access token in cookies"
        return client

