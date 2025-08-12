from app.utils.security.jwt_tokens import create_verify_token

def test_generate_verification_token():
    user_id = 123
    token = create_verify_token(user_id)

    assert isinstance(token, str)
    assert len(token) > 0
    