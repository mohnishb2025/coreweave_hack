from datetime import date
from months import add_months

def test_january_31_clips_to_february_end():
    assert add_months(date(2019, 1, 31), 1) == date(2019, 2, 28)
