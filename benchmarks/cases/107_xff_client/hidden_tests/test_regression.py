from forwards import client

def test_spaces_and_single():
    assert client(" 10.0.0.1 , 10.0.0.2 ") == "10.0.0.1"
    assert client("8.8.8.8") == "8.8.8.8"
