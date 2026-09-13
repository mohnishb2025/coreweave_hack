from datetime import date
from dates import parse

def test_january_second():
    assert parse("01/02/2003") == date(2003, 1, 2)
