from basics import user

def test_other_user_and_password_stripped():
    assert user("Basic Ym9iOnB3") == "bob"
    assert user("basic YWxpY2U6c2VjcmV0") == "alice"
