from datetime import date
from yeardays import parse

def test_common_year_and_first_day():
    assert parse("2019-365") == date(2019, 12, 31)
    assert parse("2020-001") == date(2020, 1, 1)
