from ranges import parse

def test_later_slice():
    assert parse("bytes 500-999/1234") == {"start": 500, "end": 999, "total": 1234}
    assert parse("bytes 0-0/1") == {"start": 0, "end": 0, "total": 1}
