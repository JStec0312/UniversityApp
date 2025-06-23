from jose import jwt 
from datetime import datetime, timedelta
import os
def generate_verification_token(user_id: int):
    SECRET_KEY = os.getenv("JWT_SECRET")
    data = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(minutes=60) #@TODO - change to 15 minutes   
    }
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")