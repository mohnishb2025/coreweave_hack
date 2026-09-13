from datetime import datetime, timezone
from imf import parse

def test_imf_fixdate():
    assert parse("Sun, 06 Nov 1994 08:49:37 GMT") == datetime(1994, 11, 6, 8, 49, 37, tzinfo=timezone.utc)
