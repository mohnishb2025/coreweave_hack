from datetime import date
from dates import parse

def test_december_thirteenth_and_unpadded():
    assert parse("12/13/2003") == date(2003, 12, 13)
    assert parse("2/3/2003") == date(2003, 2, 3)
