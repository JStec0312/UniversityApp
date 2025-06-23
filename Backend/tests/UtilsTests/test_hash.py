from app.utils.generate_verification_token import generate_verification_token

def test_generate_verification_token():
    user_id = 123
    token = generate_verification_token(user_id)
    
    assert isinstance(token, str)
    assert len(token) > 0
    