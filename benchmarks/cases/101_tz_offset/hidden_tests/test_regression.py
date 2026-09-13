from datetime import timedelta
from offsets import parse

def test_compact_and_negative():
    assert parse("+0530") == timedelta(hours=5, minutes=30)
    assert parse("-08:00") == timedelta(hours=-8)
