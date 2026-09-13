from ranges import parse

def test_first_five_hundred_bytes():
    assert parse("bytes 0-499/1234") == {"start": 0, "end": 499, "total": 1234}
