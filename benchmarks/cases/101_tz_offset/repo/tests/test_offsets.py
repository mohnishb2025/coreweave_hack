from datetime import timedelta
from offsets import parse

def test_half_hour_offset():
    assert parse("+05:30") == timedelta(hours=5, minutes=30)
