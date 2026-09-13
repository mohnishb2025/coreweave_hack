from datetime import date
from yeardays import parse

def test_leap_last_day():
    assert parse("2020-366") == date(2020, 12, 31)
