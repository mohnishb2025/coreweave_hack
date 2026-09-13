from datetime import datetime, timezone
from imf import parse

def test_rfc850():
    assert parse("Sunday, 06-Nov-94 08:49:37 GMT") == datetime(1994, 11, 6, 8, 49, 37, tzinfo=timezone.utc)
