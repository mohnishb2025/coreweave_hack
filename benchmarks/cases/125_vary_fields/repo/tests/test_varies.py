from varies import fields

def test_two_headers():
    assert fields("Accept-Encoding, Accept") == ["accept-encoding", "accept"]
