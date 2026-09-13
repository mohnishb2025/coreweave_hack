from basics import user

def test_alice():
    assert user("Basic YWxpY2U6c2VjcmV0") == "alice"
