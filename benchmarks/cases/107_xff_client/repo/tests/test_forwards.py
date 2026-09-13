from forwards import client

def test_leftmost_is_the_client():
    assert client("1.1.1.1, 2.2.2.2") == "1.1.1.1"
